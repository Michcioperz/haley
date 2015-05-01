#!/usr/bin/env python2

import socket, argparse, logging, threading, sys, time

LOGLEVEL_RECV = 18
LOGLEVEL_SENT = 17

logging.addLevelName(LOGLEVEL_RECV, "RECV")
logging.addLevelName(LOGLEVEL_SENT, "SENT")
logging.basicConfig(level=15, filename="haley.log", format='%(asctime)s %(levelname)s %(message)s')

class Magus(object):
    def __init__(self, haley, func, delta):
        self.haley = haley
        self.func = func
        self.delta = delta
        self.last = time.time()
    def update(self):
        if time.time() - self.last >= self.delta:
            self.last = time.time()
            try:
                self.func(self.haley)
            except:
                self.haley.say(self.haley.channel, str(sys.exc_info()[0]))


class Haley(threading.Thread):
    def __init__(self, host, port, channel, nickname):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        if "#" not in channel:
            self.channel = "#%s" % channel
        else:
            self.channel = channel
        self.nickname = nickname
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chrono = []
        self.filters = []
    def register_filter(self, priority=1):
        def func_wrapper(func):
            self.filters.append((priority,func))
            self.filters.sort()
            return func
        return func_wrapper
    def register_chrono(self, delta):
        def func_wrapper(func):
            self.chrono.append(Magus(self, func, delta))
            return func
        return func_wrapper
    def send(self, message):
        for line in message.split("\n"):
            logging.log(LOGLEVEL_SENT, "%s", line)
            self.socket.sendall("%s\r\n" % line)
    def say(self, channel, message):
        for line in message.split("\n"):
            self.send("PRIVMSG %s :%s" % (channel, line))
    def refresh(self):
        self.filters = []
        self.chrono = []
        execfile("filters.py", {"haley": self})
    def run(self):
        self.socket.connect((self.host, self.port))
        buff = ""
        while True:
            rc = self.socket.recv(512).replace("\r", "")
            buff += rc
            while "\n" in buff:
                message = buff.split("\n", 1)[0]
                buff = buff.split("\n",1)[1]
                logging.log(LOGLEVEL_RECV, message)
                if "checking ident" in message.lower():
                    self.send("USER %s %s s: %s" % (self.nickname, self.nickname, self.nickname))
                    self.send("NICK %s" % self.nickname)
                elif "nickname is already in use" in message.lower():
                    self.nickname += "_"
                    self.send("NICK %s" % self.nickname)
                elif message.upper().startswith("PING"):
                    self.send("PONG%s" % message[4:])
                elif message.startswith(":") and ("001 %s :" % self.nickname) in message and "PRIVMSG" not in message.upper():
                    self.send("JOIN %s" % self.channel)
                    self.refresh()
                elif (" PRIVMSG %s :" % self.channel) in message:
                    friend = message.split(":")[1].split(" ")[0].split("!")[0]
                    if friend != self.nickname:
                        for fill in self.filters:
                            try:
                                if fill[1](self, message.split(" PRIVMSG %s :" % self.channel, 1)[1], friend):
                                    break
                            except:
                                self.say(friend, str(sys.exc_info()[0]))
            for cron in self.chrono: cron.update()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple IRC bot")
    parser.add_argument("hostname", help="IRC server's IP or hostname")
    parser.add_argument("channel", help="Channel to mess with, leading '#' not required")
    parser.add_argument("-p", "--port", default=6667, metavar="port", help="IRC server's port")
    parser.add_argument("-n", "--name", default="hal3y", metavar="name", help="Nickname for the bot to use")
    args = parser.parse_args()
    overlord = Haley(args.hostname, args.port, args.channel, args.name)
    overlord.start()
    try:
        overlord.join()
    except KeyboardInterrupt: sys.exit()
