haley.bff = "Michcioperz"

@haley.register_filter()
def goodbye(self, message, friend):
    if self.nickname in message and "could you quit" in message.lower() and "please" in message.lower():
        if friend == self.bff:
            self.say(self.channel, "Okay, %s, see you later!" % friend)
            self.send("QUIT")
            import sys
            sys.exit()
        else:
            self.say(self.channel, "%s, it's not like you're %s, right? :D" % (friend, self.bff))
        return True
    return False

@haley.register_filter()
def refresh(self, message, friend):
    if message == "hi" or (self.nickname in message and "hi" in message):
        self.say(self.channel, "Hello, %s, so it was you making the noise up there!" % friend)
        return True
    return False

@haley.register_filter()
def refresh(self, message, friend):
    if friend == self.bff:
        if self.nickname in message and "i've found the receiver" in message.lower():
            self.refresh()
            self.say(self.channel, "Great, %s, but drop by the forge sometimes anyway! :)" % friend) 
            return True
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

@haley.register_filter()
def multeq(self, message, friend):
    if self.nickname in message and "multi" in message and "teqwve" in message:
        self.say(self.channel, "%s, heard you talking about teq's photos, right? http://ijestfajnie.pl/bin/i3 http://ijestfajnie.pl/bin/i4" % friend)
        return True
    return False
