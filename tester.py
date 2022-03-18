import pickle

class CurrentStatus:
    botLikes = True
    whichBot = -1 
    botName = ""
    reply = ""
    
    def __init__(self, whichbot):
        self.whichBot = whichbot; 
        self.botName = "A"
        pass


stEnObj = CurrentStatus(1)
print(stEnObj.botName)

strEnObjekt = pickle.dumps(stEnObj)

print(strEnObjekt)

stToObj = pickle.loads(strEnObjekt)

print(stEnObj.botName)