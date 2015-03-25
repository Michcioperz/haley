HAL3Y
=====
Welcome, citizen, to the README of Michcioperz's super awesome Internet Relay Chat bot named Hal3y.

You may think that it's named after some popular artificial intelligence named HAL9000. That's essentially bullshit. I named Hal3y after Haley from Dust: An Elysian Tail, just like @teqwve had named his bot, Hal3y's predecessor, Fidgot after Fidget from the earlier mentioned game.

Y U STOL CODES FROM TEQ UR SUCH N00B
------------------------------------
Well, I must admit teq has been a great help and I totally appreciate his work (also he's my schoolmate (and kinda senpai, but anyway)). Still, I didn't like his implementation of ruleset. It was based on regexes and vague templating he wrote himself. I myself prefer clean Python code, and this is why I decided to fork his project and redo some stuff my way.

First of all, I'm quite a fan of object-oriented programming. teq's code was almost nowhere near this. That's why I wrote stuff from scratch, keeping Fidgot code in a second tab of IDE. You could say that the basic communication with the IRC server works almost the same in both Hal3y and Fidgot, but I didn't use regexes.

Second major difference is how rulesets work. teq's way allows users to add their own rules (that are pretty interesting regexes) directly from the channel or through a private message. My way it's all different. The rules are Python functions that take a Haley object, a string with the message text and a string with the username of the person who said that. The function should return True if it's done something, or False if the command didn't match. So, if we wanted to talk about pancakes whenever they're mentioned:

```python
@haley.register_filter()
def pancakes(haley, message, user):
    if "pancakes" in message.lower():
        haley.say(haley.channel, "Pancakes? I love pancakes, %s" % user)
        return True
    return False
```

#### More docs soon
