from audioop import add
import socket
import threading
import sys
import pickle
from time import time

#from matplotlib.pyplot import connect
#from bots import *

class CurrentStatus:
    botLikes = True
    whichBot = -1 
    botName = ""
    reply = ""

class BotState: 
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.curStat = CurrentStatus()

    conn = ""
    addr = ""
    curStat = CurrentStatus()

clients = []
users = []

thisStat = CurrentStatus()

def addCli(conn, addr):
    '''for c in clients:
        if c.conn == conn:
            return'''
    thisBot = BotState(conn, addr)
    thisStat.reply = "requestInf"
    print("sending " + conn +" : "+ thisStat.reply)

    conn.send(pickle.dumps(thisStat).encode())

    thisBot.curStat = pickle.loads(conn.recv(1024).decode())

    print(thisBot.curStat.botName + " tried joining the chat!")

    for c in clients:
        if thisBot.curStat.whichBot == c.curStat.whichBot: return

    clients.append(thisBot)

#getting command line paramaters
try:
    port = int(sys.argv[1])
except:
    print("Please provide command line paramater: port")
    exit()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(("127.0.0.1", port))
    sock.listen() 
    
    while clients.__len__() < 4: 
        try:
            conn, addr = sock.accept()
            print("line 66 : " + str(conn))
            thisBot = BotState(conn, addr)
            print("line 68")
            thisStat.reply = "requestInf"
            print("line 70")
            #print("sending " + conn +" : "+ thisStat.reply)
            print("line 72")
            toSend = pickle.dumps(thisStat)
            print("line 74")
            conn.send(toSend)
            print("line 76")
            state = conn.recv(1024)
            print("line 78" + state)
            thisBot.curStat = pickle.loads(state)
            print("line 80")
            print(thisBot.curStat.botName + " tried joining the chat!")
            print("line 82")
            for c in clients:
                if thisBot.curStat.whichBot == c.curStat.whichBot: t = False

            clients.append(thisBot)
        except:
            print("Error in connecting to client")
    
    print("Everyone is here!")

    thisStat.botName = "You"
    thisStat.reply = input("Say something to initiate conversation:")
    
    sendM = pickle.dumps(thisStat)

    ########### Under here needs help
    def manyT(c):
        c.conn.send(sendM.encode())
        inMes = c.conn.recv(1024).decode()
        mes = pickle.loads(inMes)
        time.sleep((c.curStat.whichBot * 0.1) + 0.3)


    #creating multiple threads: 
    d = {}
    i = 0
    for c in clients:
        i += 1
        d["string{0}".format(i)]= threading.Thread(target=manyT, args=(c,))
        d["string{0}".format(i)].start()
        
    #joining multiple threads:
    i= 0
    for c in clients:
        i += 1
        d["string{0}".format(i)].join()


    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)



