#from argparse import Action
import random
#from random import seed
from random import randint
#import re
#import string
#import pickle
#from tokenize import String

#You can filter all characters from the string that are not printable using string.printable, like this:

#printable = set(string.printable)
#filter(lambda x: x in printable, s)

# Removing symbols and making it all lowercase, and splitting the words in an array
def formatV(a):
    stripped = a.lower()
    stripped = (c for c in stripped if (96 < ord(c) < 123) or ord(c) == 32 or ord(c) == 230 or ord(c) == 248 or ord(c) == 229 or ord(c) == 230)
    return ''.join(stripped)

#Returns a basic verb conjugation
def formatVerb(a):
    if a.__contains__("ing"):
        return a[:-3]
    elif a.__contains__("ed"):
        return a[:-2]
    else:
        return a

# Returns a verb in simple past conjugation
def formatVerbed(a):
    a = formatVerb(a)
    if a[-1] == "e":
        return a + "d"
    elif a[-1] == "y":
        return a[:-1] + "ied"
    else:
        return a + "ed"

# Returns a verb in progressive conjugation
def formatVerbing(a):
    a = formatVerb(a)
    if a[-1] == "e":
        return a[:-1] + "ing"
    else:
        return a + "ing"

botNames = ["You", "Helena", "Tobias", "Olivia", "Tom"]

class CurrentStatus:
    botLikes = True
    whichBot = 0 
    botName = ""
    reply = ""
    online = False
    verb = None
    
    def __init__(self, whichbot):
        self.whichBot = whichbot; 
        self.botName = botNames[whichbot]
        pass

class Bots:
    bot3Dislikes = ["vr", "skydive", "zipline", "bungee", "climb", "parachute"]
    greetings = ["hi", "hey", "hello", "heyy", "hello", "heyo", "heyhey", "hallais", "heylu"]
    goodbyes = ["goodbye", "seeyah", "see you later", "bye"]
    
    greeting = False
    greeted = False
    #question = False
    verb = ""
    repliedVerbs = []
    somethingToSay = False
    timesReplied = 0

    #lastPersonPositive = True

    #lastPerson = ""

    #array containing status of the other bots
    otherBots = [None] * 6
    

    def __init__(self, whichbot):
        self.status = CurrentStatus(whichbot)
        pass

    def conversation(self, inp:CurrentStatus): ## NEEDS TO RETURN BOOLEAN
        #an update on the current status of the incoming bot
        self.otherBots[inp.whichBot] = inp

        #If the reply/text part of the object is empty, no need to reply
        if inp.reply == "": 
            return False

        #Removing symbols and making it all lowercase, and splitting the words in an array
        inputWords = formatV(inp.reply).split()

        #If the incoming message contains a goodbye, this client will also say goodbye and log off. 
        for bye in self.goodbyes:
            if inp.reply.lower().__contains__(bye):
                self.status.reply += self.goodbyes[random.randint(0, len(self.goodbyes)) - 1].capitalize() + "."
                self.status.online = False
                return True

        #if this bot has replied more than three times without the user saying anything, it will not respond any more unless it is to say goodbye. 
        if inp.whichBot == 0: self.timesReplied = 0
        if self.timesReplied > 3: return False

        #If this bot hasn't greeted yet, this checks the incoming message for a greeting. If the incoming message conains a greeting, 
        #and this bot hasn't greeted yet, it adds a random greeting to the start of the current message. We also remove the greeting from the text.
        if not self.greeted:
            for greet in self.greetings:
                if inp.reply.lower().__contains__(greet):
                    self.status.reply += self.greetings[random.randint(0, len(self.greetings)) - 1].capitalize()
                    self.greeted = True
                    self.somethingToSay = True
                    inp.reply = inp.reply.replace(greet, "") #removes the greeting so it is easier to analyze the rest of the text.
                    break

        #Is the text a question?
        #self.question = inp.reply.__contains__("?")

        #For ease, assuming that the last word is the verb. 
        if len(inputWords) > 1:
            self.verb = inputWords[-1] 

        #for ease, bot funtions by number in a dictionary. 
        botFunctions = {
            1: self.bot1,
            2: self.bot2,
            3: self.bot3,
            #4: self.bot4
        }

        botFunctions[self.status.whichBot](inp)

        if self.somethingToSay == True: 
            self.timesReplied +=1
            self.status.reply += "."

        return self.somethingToSay

    #Helena, the indignant one
    def bot1(self, inp:CurrentStatus):
        #Instantiating arrays containing this bots' replies and dislikes
        dislikes =["mate", "draw", "squeeze", "train", "try", "arrive", "groan", "sound", "yell", "shade", "lick", "dare", "go for a jog", "settle", "damage", "advise", "listen", "exist", "clip", "chase", "yawn", "beam", "spell", "relax", "disagree", "brake", "unpack", "scrub", "wave", "pretend", "detect", "multiply", "exercise", "spray", "branch", "dream", "release", "suffer", "sail", "camp", "grate", "fancy", "protect", "greet", "bathe", "found", "tug", "heap", "shop", "sprout", "present", "please", "sigh", "travel", "bomb", "depend", "gather", "fence", "influence", "carve", "owe", "cheat", "delay", "rot", "offer", "rock", "precede", "frighten", "whirl", "tap", "reflect", "help", "frame", "share", "form", "race", "bow", "flash", "bat", "bless", "stain", "crush", "wait", "deliver", "vanish", "recognise", "agree", "dust", "smile", "guess", "claim", "juggle", "store", "cure", "deceive", "rejoice", "mix", "compete", "tour", "sin"]
        positiveReplies = ["I'm totally in :D", "oooh {}, I wanna go".format(formatVerbing(self.verb)), "yes, can we go right away?? :D"]
        negativeReplies = ["I suck at {}, can't we do something else? :/".format(formatVerbing(self.verb)), "meh", ":/", "Why {} though?".format(formatVerbing(self.verb))]
        indignantReplies = []
        indignantReplies.append(inp.botName + ", come onnn, live a little, I know you want to {}!".format(formatVerb(self.verb)))
        indignantReplies.append("don't be so boring " + inp.botName)
        indignantReplies.append("aww, come on " + inp.botName)

        #If there is a verb to respond to that is not yet responded to:
        if not (self.verb == "" or self.repliedVerbs.__contains__(self.verb)):
            #checks if the incoming message contains a verb this bot doesn't like, and sets botLikes to False if they don't 
            self.status.botLikes = not dislikes.__contains__(self.verb)

            if self.status.botLikes:
                addition = positiveReplies[randint(0, len(positiveReplies) -1)]
            else: 
                addition = negativeReplies[randint(0, len(negativeReplies) -1)]
            
            if len(self.status.reply) > 1: 
                self.status.reply += ", "
            else:
                addition.capitalize()

            self.status.reply += addition

            self.somethingToSay = True
            
        #If another bot doesn't like something bot1 likes, they will be indignant about that and might complain
        if inp.botLikes == False and self.status.botLikes and randint(0, 1) == 0:
            addition = indignantReplies[randint(0, len(indignantReplies) - 1)]
            
            if len(self.status.reply) > 1: 
                self.status.reply += ", "
            else:
                addition.capitalize()

            self.status.reply += addition

            self.somethingToSay = True
            
    #Tobias
    def bot2(self, inp:CurrentStatus):
        dislikes = ["suspend", "sip", "whirl", "polish", "perform", "box", "applaud", "draw", "desert", "decorate", "object", "beam", "report", "fry", "go for a jog", "scare", "dislike", "prepare", "dance", "steer", "squash", "land", "warn", "knit", "rejoice", "delight", "surprise", "attempt", "license", "refuse", "pull", "order", "camp", "laugh", "hug", "alert", "bolt", "clip", "ban", "stroke", "battle", "miss", "program", "telephone", "concern", "consist", "slap", "love", "roll", "fax", "exercise", "spark", "whisper", "spill", "remind", "increase", "connect", "screw", "preserve", "describe", "pedal", "destroy", "cycle", "interest", "bare", "store", "encourage", "dream", "excite", "glue", "transport", "sign", "kill", "label", "inform", "mess up", "attend", "coach", "consider", "blink", "compete", "raise", "bleach", "attract", "offer", "tempt", "rely", "stain", "rescue", "obtain", "guide", "heal", "judge", "scrub", "race", "film", "suppose", "lick", "double", "grease"]
        
        for x in dislikes:
            if self.verb == x:
                bot2Likes = False 
                break
        
        if bot2Likes and self.status.botLikes:
            return "Yay, let's {} then!".format(a)
        elif bot2Likes:
            return "Hey, I really wanted to {}, I can teach you if you want.".format(a)
        elif self.status.botLikes:
            return "Meh, I just {} and it sucked".format(formatVerbed(a))
        else:
            return "Yeah, no, let's do something else, {} not really that much fun.".format(formatVerbing(a))

            '''elif b == 2:
            if bot2Likes and self.bot3Likes :
                return "Hahaha, for sure, " + self.bot3Name + " and heigts are a terrible idea."        '''

    def bot3(self, a, b=None): ## THE # QUEEN
        for x in self.array3:
            if x == a:
                bot3Likes = False
                break
        if not bot3Likes:
            return "No way I'm doing {}, I can watch, but I'd honestly be sick all over everyone.".format(formatVerbing(a)) 
        elif self.bot2Likes:
            return "Hey, I'm in if " + self.bot2Name + "'s in, as long as it's not {} I'm good haha".format(formatVerbing(random.choice(self.array3)))
        else:
            bot3Likes = False
            return "Idk guys, seems a bit lame if not everyone wants to do it. {} can be fun some times, but it gets boring real fast. Another time?".format(formatVerbing(a.capitalize()))

        