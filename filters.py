# encoding: utf-8
from pymarkovchain import MarkovChain
import os.path, logging, re, random
haley = haley
haley.bffs = ["Michcioperz","Michcioperz480"]
haley.mode = False
haley.song = None
haley.send("AWAY :Airi")
with open(os.path.expanduser("~/.haleyay.txt")) as f:
    haley.markov_text = f.read()
haley.markov_db = MarkovChain(os.path.expanduser("~/.haleyay.db"))

@haley.register_filter(-100)
def nofidgot(self, message, friend):
    if friend == "fidgot" or message.startswith("fidgot"): return True
    return False

@haley.register_filter()
def modeswitch(self, message, friend):
    if ("ACTION taps %s's head" % self.nickname) in message:
        if self.mode:
            self.say(self.channel, "Leaving Sister Centipede mode.")
            self.send("AWAY :Airi")
        else:
            self.say(self.channel, "Entering Sister Centipede mode.")
            self.send("AWAY :Sister Centipede")
        self.mode = not self.mode
        return True
    return False

@haley.register_filter(97)
def marcollect(self, message, friend):
    self.markov_text += "\n"+message
    return False

@haley.register_filter()
def margen(self, message, friend):
    if self.nickname in message and self.mode and "markov regenerate" in message:
        with open(os.path.expanduser("~/.haleyay.txt"), 'w') as f:
            file.write(self.markov_text)
        self.markov_db.generateDatabase(self.markov_text)
        if self.mode:
            self.say(self.channel, "Markov's chain database regenerated.")
        else:
            self.say(self.channel, "Sure thing!")
        return True
    return False

@haley.register_chrono(160)
def marbackup(self): 
    with open(os.path.expanduser("~/.haleyay.txt"), 'w') as f:
        file.write(self.markov_text)
    self.markov_db.generateDatabase(self.markov_text)
    logging.info("markov db backed up")

@haley.register_filter()
def marsay(self, message, friend):
    if not self.mode and self.nickname in message and "say" in message and "something" in message:
        times = re.search("(?P<tim>\d+) times", message)
        if times:
            times = int(times.group("tim"))
        else:
            times = 1
        for t in range(times): self.say(self.channel, self.markov_db.generateString())
        return True
    return False

@haley.register_filter()
def goodbye(self, message, friend):
    if self.nickname in message and "quit" in message.lower() and (self.mode or "please" in message.lower()):
        if friend in self.bffs:
            if self.mode:
                self.say(self.channel, "Commencing logout.")
            else:
                self.say(self.channel, "Okay, %s, see you later!" % friend)
            self.send("QUIT :Bye!")
            import sys
            sys.exit()
        else:
            if self.mode:
                self.say(self.channel, "Insufficent privileges.")
            else:
                self.say(self.channel, "%s, it's not like you're %s, right? :D" % (friend, self.bff))
        return True
    return False

@haley.register_filter(1)
def tell(self, message, friend):
    if message.startswith(self.nickname):
        if message.split(" ",1)[1].startswith("tell "):
            if friend in self.bffs:
                spl = message.split(" ",3)
                self.say(self.channel, "%s: %s" % (spl[2], spl[3]))
            else:
                if self.mode:
                    self.say(self.channel, "Insufficent privileges.")
                else:
                    self.say(self.channel, "%s, I can't be easily convinced by someone I barely know ;)" % friend)
            return True
    return False

@haley.register_filter(2)
def thanks(self, message, friend):
    if not self.mode and self.nickname in message and ("thanks" in message.lower() or "thank you" in message.lower()):
        self.say(self.channel, "You're welcome, %s!" % friend)
        return True
    return False

@haley.register_filter()
def how_are_you(self, message, friend):
    if not self.mode and self.nickname in message and ("how are you" in message.lower() or "what's up" in message.lower()):
        self.say(self.channel, "The business's fine, %s! And you?" % friend)
        return True
    return False

@haley.register_filter()
def hello(self, message, friend):
    if not self.mode and message.lower() == "hi" or (self.nickname in message and "hi" in message.lower().split()):
        self.say(self.channel, random.choice(["%s! Tutturuuu!","Hello, %s, so it was you making the noise up there!"]) % friend)
        return True
    return False

@haley.register_filter()
def refresh(self, message, friend):
    if self.nickname in message and ((not self.mode and "the receiver" in message.lower()) or (self.mode and "refresh" in message.lower())):
        if friend in self.bffs:
            if self.mode:
                self.say(self.channel, "Commands assignment refreshed. Leaving Sister Centipede mode.")
            else:
                self.say(self.channel, "Great, %s, but drop by the forge sometimes anyway! :)" % friend)
            self.refresh()
        else:
            if self.mode:
                self.say(self.channel, "Insufficent privileges.")
            else:
                self.say(self.channel, "%s, what receiver?" % friend)
        return True
    return False

@haley.register_filter()
def nanon(self, message, friend):
    if "nano" in message.lower() or "hakase" in message.lower():
        if "nano" in message.lower():
            self.say(self.channel, "HAKASE"*len(re.findall("nano", message.lower())))
        if "hakase" in message.lower():
            self.say(self.channel, "NANO"*len(re.findall("hakase", message.lower())))
        return True
    return False

@haley.register_filter(99)
def not_understand(self, message, friend):
    if self.nickname in message:
        if self.mode:
            self.say(self.channel, "Command not understood.")
        else:
            self.say(self.channel, random.choice(["Yes, it's me. The Organization's feeding me phony data through %s. El Psy Kongroo.","Hey, %s, I didn't quite get what you mean?"]) % friend)
        return True
    return False
