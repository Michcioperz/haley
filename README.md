fidgot
======
simple irc bot in python

##usage
see:

    ./fidgot.py --help

##rules
Rule is a pair of regular expression and response, when fidgot receives a message that matches given regex she evaluate response and use it. There can be only one rule per line, rules are checked from top to down, and only the first rule that matches is used.
    
Fidgot uses python [re](https://docs.python.org/2/library/re.html "re") regular expression module, so you can use all it features in rules.
    
To insert a group put it's name inside <...>, for example:

    "!say (.*)"         "<1>"
    "!say (?P<msg>.*)"  "<msg>"

To use a flag in this rule put it just before regular expression:

    r"!do (.)"          "<1>"
current flags:
- r     do not escape characters in message from user
    
##variables
To define a variable put in into a rules file:

    $var    = "variable"
    
To use it in rule simple put it's name with $ inside a rule, you can use it both in regular expression or response.

    "!var"              "$var"

Some predefined variables, that you can use every time is:
- $name   - name of bot
- $chan   - current channel (in private messages it's user nickname)
- $user   - user who has wrote to fidgot
    
In fact, variable body is evaluated in moment it's assigned, so you can use variables and functions in it.

##functions
To use function put it's name inside a rule with leading $.

    "!foo"              "$nop(foo)"
    "!foo2"             "$nop($nop(foo))"
    "!foo3"             "$nop(output of nop - $nop(foo))"
    
###availible functions:
- nop         does nothing, returns it's input
- add\_rule   adds new rule, same syntax as in rules file
- list\_rules list all rules
- del\_rule   delete rule
