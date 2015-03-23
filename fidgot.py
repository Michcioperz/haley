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

def nop(line):
    return line

rules=[]
variables={}
functions={"nop" : nop}
sbst=[('\\\\', '\\'), ('\\"', '"'), ('\\<', '<'), 
        ('\\>', '>'), ('\\(', '('), ('\\)', ')'),
        ('\\$', '$')]
def substitute(s):
    for (r, p) in sbst:
        s=s.replace(r, p)
    return s
def escape(s):
    for (r, p) in sbst:
        s=s.replace(p, r)
    return s

class Rule:
    def __init__(self, rgxp, resp, flags):
        self.rgxp, self.resp, self.flags = rgxp,resp, flags
    def flag(self, flag):
        for x in flag:
            if self.flags.find(x) == -1:
                return False
        return True

def add_rule(rgxp, resp, flags):
    if rgxp[0] != '^':
        rgxp = '^'+rgxp
    if rgxp[-1] != '$':
        rgxp += '$'
    print 'new rule', rgxp, ' -- ', flags, ' -- ', resp
    rules.append(Rule(rgxp, resp, flags))
def set_var(name, value):
    variables[name]=value
    print 'new value $%s = %s'%(name, value)
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
        line=line.strip()
        rgxp = re.match(r'^(?P<flags>\w*)"(?P<rgxp>.*[^\\](\\\\)*)"\s*"(?P<resp>.*)"\s*$', line)
        if rgxp:
            add_rule(rgxp.group("rgxp"), rgxp.group("resp"), rgxp.group("flags"))
            continue
        rgxp = re.match(r'^\$(?P<name>\w+)\s*=\s*"(?P<value>.*)"$', line)
        if rgxp:
            set_var(rgxp.group('name'), substitute(process(rgxp.group('value'))))
            continue
        if line[0] != '#' and re.match(r'^\s*$', line) == None:
            print "syntax error in", filename, "line", num

def process(msg):
    prev, escaped = None, [False for i in range(len(msg)+1)]
    for i in range(len(msg)):
        if prev == '\\' and not escaped[i-1]:
            escaped[i] = True
        prev = msg[i]

    next_bracket = [-1 for i in range(len(msg)+1)]
    for i in range(len(msg))[::-1]:
        if not escaped[i] and msg[i] == '(':
            next_bracket[i] = i
        else:
            next_bracket[i] = next_bracket[i+1]

    depth, first, pair = 0, [0 for i in range(len(msg)+1)], [-1 for i in range(len(msg)+1)]
    for i in range(len(msg)):
        if not escaped[i]:
            if msg[i] == '(':
                depth += 1
                first[depth] = i
            elif msg[i] == ')':
                pair[first[depth]] = i
                pair[i] = first[depth]
                depth -= 1

    i, keyword, name, ret = 0, False, "", ""
    while i < len(msg):
        if keyword:
            if re.match(r'^\w$', msg[i]):
                name += msg[i]
            else:
                keyword = False
                if name in variables.keys():
                    ret += var(name) + msg[i]
                elif name in functions.keys():
                    ret += foo(name, process(msg[next_bracket[i]+1:pair[next_bracket[i]]]))
                    i = pair[next_bracket[i]]
        else:
            if msg[i] == '$' and not escaped[i]:
                keyword = True
                name=""
            else:
                ret += msg[i]
        i += 1
    return ret

def var(name):
    if name not in variables.keys():
        return "NOVAR"
    return variables[name]
def foo(name, args):
    if name not in functions:
        return "NOFUN"
    return functions[name](args)

def response(chan, user, rawmsg):
    variables['user']=user
    variables['chan']=chan
    escmsg=escape(rawmsg)
    for rule in rules:
        rgxp=substitute(process(rule.rgxp))
        if rule.flag('r'):
            m=re.match(rgxp, rawmsg)
        else:
            m=re.match(rgxp, escmsg)
        if m:
            parts=re.split(r"([^\\](\\\\)*)(<[^>]+>)", ' '+rule.resp)
            for i in range(len(parts)):
                if parts[i] == None:
                    parts[i]=""
                elif len(parts[i]) >= 3 and parts[i][0] == '<' and parts[i][-1] == '>':
                    expr=parts[i][1:-1].strip()
                    try:
                        parts[i]=m.group(int(expr))
                    except:
                        try:
                            parts[i]=m.group(expr)
                        except:
                            parts[i]=""
            resp=substitute(process("".join(parts)))
            if len(resp)>0:
                say(chan, resp[1:])
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
    PORT=int(args["port"])
    variables['name']=NAME=args["name"]
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

            if re.search(r"Checking Ident", msg, re.IGNORECASE):
               send("user %s %s s: %s\nnick %s"%(
                   NAME, NAME, NAME, NAME))
            elif re.search(r"Nickname is already in use", msg, re.IGNORECASE):
                NAME += "_"
                send("nick %s"%NAME)
            elif re.match(r"PING.*", msg, re.IGNORECASE):
                send("PONG%s"%re.search("PING(?P<ping>.*)", msg, re.IGNORECASE).group("ping"))
            elif re.match(r":[^:]*001 %s :.*"%NAME, msg):
                send("join %s"%CHAN)
            elif re.match(r":[^\s]* PRIVMSG %s.*"%CHAN, msg):
                rgxp = re.match(r":(?P<nick>[^\s!]*)(![^\s]*)* PRIVMSG %s :(?P<msg>.*)$"%CHAN, msg)
                if rgxp:
                    response(CHAN, rgxp.group("nick"), rgxp.group("msg"))
            elif PRIV and re.match(r":[^\s]* PRIVMSG %s.*"%NAME, msg):
                rgxp = re.match(r":(?P<nick>[^\s!]*)(![^\s]*)* PRIVMSG %s :(?P<msg>.*)$"%NAME, msg)
                if rgxp:
                    response(rgxp.group("nick"), rgxp.group("nick"), NAME+" "+rgxp.group("msg"))

if __name__ == "__main__":
    main()
