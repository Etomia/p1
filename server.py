from audioop import add
import socket
import threading
import sys
import pickle
import time

class CurrentStatus:
    botLikes = True
    whichBot = -1 
    botName = "ServerMessage"
    reply = ""
    online = False

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
respondQueue = []

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

    thisStat.online = True
    print("This server is now running, you can access it on the IP: 127.0.0.1, and the port " + str(port))
    
    while len(clients) < 5: 
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
                    break

            if not thisBot.accepted:
                print(thisBot.curStat.botName + " is already connected, terminating connection to client.")
                conn.send(b"badBot")
            else:   
                clients.append(thisBot)
                conn.send(b"goodBot")
                thisStat.reply = thisBot.curStat.botName + " has joined the chat!"
                
                print(thisStat.reply)
                for c in clients:
                    c.conn.send(pickle.dumps(thisStat))

        except Exception as e:
            print("Error in connecting to client" + str(e))
    
    print("Everyone is here!")

    '''thisStat.botName = "You"
    thisStat.reply = input("Say something to initiate conversation:")
    
    sendM = pickle.dumps(thisStat)

    respondQueue.append(sendM)'''

    #Creating method to receive, which will be multithreaded for the different clients
    def clientT(c):
        while True:
            inMes = c.conn.recv(1024)
            respondQueue.append(inMes) #Python Lists are relatively thread-safe as long as you don't change the same values

    #Method to send to clients
    def sendT():
        print("running sendT()")
        while True:
            time.sleep(0.3) #Making sure this is not constantly busying the list by checking length
            print("continuing to run sendT()")
            if len(respondQueue) > 0: 
                print("ready to send")
                mesP = respondQueue.pop(0) #getting the first item from the list
                mes = pickle.loads(mesP)

                print(mes.botName + ": \t" + mes.reply) #printing the message
            
                #Finding the client that sent this message and changing its current status. Sending every other client the message.
                for c in clients:
                    if c.curStat.whichBot == mes.whichBot:
                        c.curStat = mes
                    else:
                        c.conn.send(mesP)


    #creating and starting a thread to send from:
    sendThread = threading.Thread(target=sendT)
    sendThread.start()

    #creating and starting multiple threads for receiving from clients: 
    d = {}
    i = 0
    for c in clients:
        i += 1
        d["cli{0}".format(i)]= threading.Thread(target=clientT, args=(c,))
        d["cli{0}".format(i)].start()
        
    #joining multiple threads:
    sendThread.join()
    i= 0
    for c in clients:
        i += 1
        d["cli{0}".format(i)].join()

