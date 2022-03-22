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

    accepted = True
    conn = ""
    addr = ""
    curStat = CurrentStatus()

clients = []
users = []

thisStat = CurrentStatus()

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
            
            thisBot = BotState(conn, addr)
            
            thisStat.reply = "requestInf"
            
            toSend = pickle.dumps(thisStat)
            
            conn.send(toSend)
            
            pickledState = conn.recv(1024)
            
            thisBot.curStat = pickle.loads(pickledState)
            
            print(thisBot.curStat.botName + " tried joining the chat!")
            
            for c in clients:
                if thisBot.curStat.whichBot == c.curStat.whichBot:
                    thisBot.accepted = False
                    #conn.send(pickle.dumps(thisStat))
                    break

            if not thisBot.accepted:
                print(thisBot.curStat.botName + " is already connected, terminating connection to client.")
                conn.send(b"badBot")
            else:   
                clients.append(thisBot)
                conn.send(b"goodBot")
                print(thisBot.curStat.botName + " has joined the chat!")

        except Exception as e:
            print("Error in connecting to client" + str(e))
    
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



