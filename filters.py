# enxodimg: utf-8
from pymarkovchain import MarkovChain
import os.path, logging
haley.bffs = ["Michcioperz","Michcioperz480"]
with open(os.path.expanduser("~/.haleyay.txt")) as file:
    haley.markov_text = file.read()
haley.markov_db = MarkovChain(os.path.expanduser("~/.haleyay.db"))

@haley.register_filter(97)
def marcollect(self, message, friend):
    self.markov_text += "\n"+message
    return False

@haley.register_filter()
def margen(self, message, friend):
    if self.nickname in message and "regenerate" in message:
        with open(os.path.expanduser("~/.haleyay.txt"), 'w') as file:
            file.write(self.markov_text)
        self.markov_db.generateDatabase(self.markov_text)
        self.say(self.channel, "Sure")
        return True
    return False

@haley.register_chrono(160)
def marbackup(self): 
    with open(os.path.expanduser("~/.haleyay.txt"), 'w') as file:
        file.write(self.markov_text)
    self.markov_db.generateDatabase(self.markov_text)
    logging.info("markov db backed up")

@haley.register_filter()
def marsay(self, message, friend):
    if self.nickname in message and "say something" in message:
        self.say(self.channel, self.markov_db.generateString())
        return True
    return False

@haley.register_filter()
def goodbye(self, message, friend):
    if self.nickname in message and "quit" in message.lower() and "please" in message.lower():
        if friend in self.bffs:
            self.say(self.channel, "Okay, %s, see you later!" % friend)
            self.send("QUIT :Bye!")
            import sys
            sys.exit()
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
                self.say(self.channel, "%s, I can't be easily convinced by someone I barely know ;)" % friend)
            return True
    return False

@haley.register_filter(2)
def thanks(self, message, friend):
    if self.nickname in message and ("thanks" in message.lower() or "thank you" in message.lower()):
        self.say(self.channel, "You're welcome, %s!" % friend)
        return True
    return False

@haley.register_filter()
def how_are_you(self, message, friend):
    if self.nickname in message and ("how are you" in message.lower() or "what's up" in message.lower()):
        self.say(self.channel, "The business's fine, %s! And you?" % friend)
        return True
    return False

@haley.register_filter()
def hello(self, message, friend):
    if message == "hi" or (self.nickname in message and " hi " in message):
        self.say(self.channel, "Hello, %s, so it was you making the noise up there!" % friend)
        return True
    return False

@haley.register_filter()
def refresh(self, message, friend):
    if self.nickname in message and "the receiver" in message.lower():
        if friend in self.bffs:
            self.refresh()
            self.say(self.channel, "Great, %s, but drop by the forge sometimes anyway! :)" % friend) 
        else:
            self.say(self.channel, "%s, what receiver?" % friend)
        return True
    return False

@haley.register_filter(99)
def not_understand(self, message, friend):
    if self.nickname in message:
        self.say(self.channel, "Hey, %s, I didn't quite get what you mean?" % friend)
        return True
    return False

@haley.register_filter(3)
def multeq(self, message, friend):
    if self.nickname in message and "multi" in message and "teqwve" in message:
        self.say(self.channel, "%s, heard you talking about teq's photos, right? http://ijestfajnie.pl/bin/i3 http://ijestfajnie.pl/bin/i4" % friend)
        return True
    return False
