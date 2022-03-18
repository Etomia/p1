from argparse import Action
import random
import string
import pickle

#You can filter all characters from the string that are not printable using string.printable, like this:

#printable = set(string.printable)
#filter(lambda x: x in printable, s)


def formatV(a):
   # Returns the string with only alphabetical letters and spaces, including æøå
    stripped = (c for c in a if (64 < ord(c) < 123) or ord(c) == 32 or ord(c) == 230 or ord(c) == 248 or ord(c) == 229 or ord(c) == 198 or ord(c) == 216 or ord(c) == 230 or ord(c) == 197)
    return ''.join(stripped)

def formatVerbed(a):
    if a[-1] == "e":
        return a + "d"
    elif a[-1] == "y":
        return a[:-1] + "ied"
    else:
        return a + "ed"

def formatVerbing(a):
    if a[-1] == "e":
        return a[:-1] + "ing"
    else:
        return a + "ing"

botNames = ["Helena", "Tobias", "Olivia", "Tom"]
array1 =["mate", "draw", "squeeze", "train", "try", "arrive", "groan", "sound", "yell", "shade", "lick", "dare", "go for a jog", "settle", "damage", "advise", "listen", "exist", "clip", "chase", "yawn", "beam", "spell", "relax", "disagree", "brake", "unpack", "scrub", "wave", "pretend", "detect", "multiply", "exercise", "spray", "branch", "dream", "release", "suffer", "sail", "camp", "grate", "fancy", "protect", "greet", "bathe", "found", "tug", "heap", "shop", "sprout", "present", "please", "sigh", "travel", "bomb", "depend", "gather", "fence", "influence", "carve", "owe", "cheat", "delay", "rot", "offer", "rock", "precede", "frighten", "whirl", "tap", "reflect", "help", "frame", "share", "form", "race", "bow", "flash", "bat", "bless", "stain", "crush", "wait", "deliver", "vanish", "recognise", "agree", "dust", "smile", "guess", "claim", "juggle", "store", "cure", "deceive", "rejoice", "mix", "compete", "tour", "sin"]
array2 = ["suspend", "sip", "whirl", "polish", "perform", "box", "applaud", "draw", "desert", "decorate", "object", "beam", "report", "fry", "go for a jog", "scare", "dislike", "prepare", "dance", "steer", "squash", "land", "warn", "knit", "rejoice", "delight", "surprise", "attempt", "license", "refuse", "pull", "order", "camp", "laugh", "hug", "alert", "bolt", "clip", "ban", "stroke", "battle", "miss", "program", "telephone", "concern", "consist", "slap", "love", "roll", "fax", "exercise", "spark", "whisper", "spill", "remind", "increase", "connect", "screw", "preserve", "describe", "pedal", "destroy", "cycle", "interest", "bare", "store", "encourage", "dream", "excite", "glue", "transport", "sign", "kill", "label", "inform", "mess up", "attend", "coach", "consider", "blink", "compete", "raise", "bleach", "attract", "offer", "tempt", "rely", "stain", "rescue", "obtain", "guide", "heal", "judge", "scrub", "race", "film", "suppose", "lick", "double", "grease"]
array3 = ["vr", "skydive", "zipline", "bungee"]
greetings = ["Hi", "Hi", "Hello", "Hei", "Hallo", "Heihei", "Heii", "hi", "hi", "hello", "hei", "hallo", "heihei", "heii"]

class CurrentStatus:
    botLikes = True
    whichBot = -1 
    botName = ""
    reply = ""
    
    def __init__(self, whichbot):
        self.whichBot = whichbot; 
        self.botName = botNames[whichbot]
        pass

class Bots:
    def __init__(self, whichbot):
        self.greeting = False
        self.question = False
        self.lastPersonPositive = True
        self.verb = ""

        self.lastPerson = ""

        '''self.bot1Name = "Helena"
        self.bot2Name = "Tobias"
        self.bot3Name = "Olivia"
        self.bot4Name = "Tom"'''

        self.otherBotsLike = [True, True, True, True]
        
        '''self.bot1Likes = True
        self.bot2Likes = True
        self.bot3Likes = True
        self.bot4Likes = True'''

        self.status = CurrentStatus(whichbot)
        pass


    def conversation(self, inputS):
        inp = pickle.loads(inputS)

        if inp.reply == "": 
            return ""

        inputWords = inp.reply.split()

        self.lastPerson = inp.whichBot

        firstWord = inputWords[1]

        if self.greetings.__contains__(firstWord):
            self.greeting = True

        if inputWords.__contains__("yes") or inputWords.__contains__("Yes"):
            self.lastPersonPositive

        action = formatV(action)

        if action == None:
            return ""

        return pickle.dumps(self.status)
        #print("\nMe: Do you guys want to {}? \n".format(action)) 
        #print(self.bot1Name + ": {}".format(bot1(action)))
        #print(bot2Name + ": {}".format(bot2(action)))
        #print(bot3Name + ": {}".format(bot3(action)))
        #print(bot2Name + ": {}".format(bot2(action, 2)))
        #print(bot1Name + ": {}".format(bot1(action, 2)))
        #print(bot4Name + ": {}".format(bot4(action))) 


    def bot1(self, a, b = None):
        if b == None:
            for x in self.array1:
                if a == x:
                    self.bot1Likes = False 
                    break

            if self.bot1Likes:
                return "I'm totally in :D"
            else: 
                return "I suck at {}, can't we do something different? :/".format(formatVerbing(a))
        
        if b == 2:
            if self.bot1Likes and not self.bot2Likes:
                return self.bot3Name + ", come onnn, live a little, I know you want to {}!".format(a)

            
    def bot2(self, a, b = None):
        if b == None:
            for x in self.array2:
                if a == x:
                    bot2Likes = False 
                    break
            
            if bot2Likes and self.bot1Likes:
                return "Yay, let's {} then!".format(a)
            elif bot2Likes:
                return "Hey, I really wanted to {}, I can teach you if you want.".format(a)
            elif self.bot1Likes:
                return "Meh, I just {} and it sucked".format(formatVerbed(a))
            else:
                return "Yeah, no, let's do something else, {} not really that much fun.".format(formatVerbing(a))

        elif b == 2:
            if bot2Likes and self.bot3Likes :
                return "Hahaha, for sure, " + self.bot3Name + " and heigts are a terrible idea."        

    def bot3(self, a, b=None):
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
