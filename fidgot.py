#!/usr/bin/env python2

import socket, re, random, argparse
from time import sleep

HOST=CHAN=PORT=NAME=None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(msg):
    for m in msg.split("\n"):
        print "<", m
        s.sendall("%s\r\n"%m)
def say(msg):
    for m in msg.split("\n"):
        send("PRIVMSG %s :%s"%(CHAN, m))

def response(user, msg):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple irc bot")
    parser.add_argument("hostname", help="irc server address")
    parser.add_argument("channel", help="destination channel, leading '#' isn't required")
    parser.add_argument("-p", "--port", default=6667, metavar="port",
            help="port to use, default 6667")
    parser.add_argument("-n", "--name", default="pbot", metavar="name",
            help="bot's irc nickname. default pbot")
    args=vars(parser.parse_args())

    HOST=args["hostname"]
    PORT=args["port"]
    NAME=args["name"]
    CHAN=args["channel"]
    if CHAN[0] != '#':
        CHAN = '#'+CHAN

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
                response(rgxp.group("nick"), rgxp.group("msg"))
