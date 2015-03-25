haley.bff = "Michcioperz"

@haley.register_filter()
def goodbye(self, message, friend):
    if self.nickname in message and "quit" in message.lower() and "please" in message.lower():
        if friend == self.bff:
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
            if friend == self.bff:
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
    if message == "hi" or (self.nickname in message and "hi" in message):
        self.say(self.channel, "Hello, %s, so it was you making the noise up there!" % friend)
        return True
    return False

@haley.register_filter()
def refresh(self, message, friend):
    if self.nickname in message and "the receiver" in message.lower():
        if friend == self.bff:
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
