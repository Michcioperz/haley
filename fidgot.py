#!/usr/bin/env python2

import socket, re, random, argparse
from time import sleep

HOST=CHAN=PORT=NAME=PRIV=None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(msg):
    for m in msg.split("\n"):
        print "<", m
        s.sendall("%s\r\n"%m)
def say(chan, msg):
    for m in msg.split("\n"):
        send("PRIVMSG %s :%s"%(chan, m))

rules={}
sbst=[('\\\\', '\\'), ('\\"', '"')]
def add_rule(rgxp, resp):
    for (p, s) in sbst:
        rgxp=rgxp.replace(p, s)
        resp=resp.replace(p, s)
    if rgxp[0] != '^':
        rgxp = '^'+rgxp
    if rgxp[-1] != '$':
        rgxp += '$'
    print 'new rule', rgxp, ' --- ', resp
    rules[rgxp] = resp
def load_rules(filename):
    buf, num, f = "", 0, open(filename)
    for line in f:
        num += 1
        line = buf+line.replace('\n', '')
        if len(line) == 0:
           continue
        if line[-1] == '\\' and line[0] != '#':
            buf = line[:-1]
            continue
        buf = ""
        if line[0] != '#':
            rgxp = re.match(r'^"(?P<rgxp>.*(\\\\)*[^\\]*)"\s*"(?P<resp>.*(\\\\)*[^\\]*)"$', line)
            if rgxp:
                add_rule(rgxp.group("rgxp"), rgxp.group("resp"))
            else:
                print "syntax error in", filename, "line", num

def response(chan, user, msg):
    for rgxp, resp in rules.iteritems():
        m=re.match(rgxp, msg)
        if m:
            say(chan, resp)
            return

def main():
    parser = argparse.ArgumentParser(description="Simple irc bot")
    parser.add_argument("hostname", help="irc server address")
    parser.add_argument("channel", help="destination channel, leading '#' isn't required")
    parser.add_argument("-p", "--port", default=6667, metavar="port",
            help="port to use, default 6667")
    parser.add_argument("-n", "--name", default="fidgot", metavar="name",
            help="bot's irc nickname. default fidgot")
    parser.add_argument("-r", "--rules", default="~/.fidgot.rules", metavar="filename",
            help="file with bot's responses")
    parser.add_argument("--priv", action="store_true", 
            help="enable provate messages parsing")
    args=vars(parser.parse_args())

    HOST=args["hostname"]
    PORT=args["port"]
    NAME=args["name"]
    PRIV=args["priv"]
    CHAN=args["channel"]
    if CHAN[0] != '#':
        CHAN = '#'+CHAN
    load_rules(args["rules"])

    s.connect((HOST, PORT))
    
    buf = ""
    while True:
        msg = s.recv(512).replace("\r", "")
        buf += msg

        while buf.find("\n") != -1:
            msg = buf[:buf.find("\n")]
            buf = buf[buf.find("\n")+1:]
            print ">", msg

            if re.search("Checking Ident", msg, re.IGNORECASE):
               send("user %s %s s: %s\nnick %s"%(
                   NAME, NAME, NAME, NAME))
            elif re.search("Nickname is already in use", msg, re.IGNORECASE):
                NAME += "_"
                send("nick %s"%NAME)
            elif re.match("PING.*", msg, re.IGNORECASE):
                send("PONG%s"%re.search("PING(?P<ping>.*)", msg, re.IGNORECASE).group("ping"))
            elif re.match(":[^:]*001 %s :.*"%NAME, msg):
                send("join %s"%CHAN)
            elif re.match(":[^:]*PRIVMSG %s.*"%CHAN, msg):
                rgxp = re.match(":(?P<nick>\w*)![^:]*:(?P<msg>.*)", msg)
                response(CHAN, rgxp.group("nick"), rgxp.group("msg"))
            elif PRIV and re.match(":[^:]*PRIVMSG %s.*"%NAME, msg):
                rgxp = re.match(":(?P<nick>\w*)[^:]*:(?P<msg>.*)", msg)
                response(rgxp.group("nick"), rgxp.group("nick"), NAME+" "+rgxp.group("msg"))

if __name__ == "__main__":
    main()
