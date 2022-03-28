import socket
import threading
import sys
from bots import *
import time

messagesIn = []

#Getting command line parameters
try:
    host = sys.argv[1]
    port = int(sys.argv[2])
    thisBotIN = sys.argv[3]
except:
    print("Please provide command line paramaters in the following order: host port botNumber(1-4) if you want this to be a user-client, write 0 in the botnumber slot")
    exit()

#Checking if correct bot nr is provided
while (not thisBotIN.isnumeric()) or int(thisBotIN) < 0 or int(thisBotIN) > 4:
    thisBotIN = input("Write only, 0, 1, 2, 3, or 4 to exit write E: ")

    if thisBotIN == "E" or thisBotIN == "e":
        exit()

#starting new bots object
convo = Bots(int(thisBotIN))

#Connects the socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    print("Connected to server!")

    #listens for answer:
    initiateAnswer = sock.recv(1024)
    print("Received from server!")

    initialMsg = pickle.loads(initiateAnswer)
    print(initialMsg.reply)

    print("sending...")
    sendObj = pickle.dumps(convo.status)
    sock.send(sendObj)
    print("sent!")

    acc = sock.recv(1024)
    if acc == b"badBot":
        print("This bot already exists, start again and use a different bot number.")
        exit()
    elif acc == b"goodBot": 
        convo.status.online = True
        print("Accepted, this bot is now connected!")

    #Creating a queue for everything incoming from server, this is so client can still receive from server if client is working on something else
    incomingQueue = []

    def receive():   
        print("receive thread open")   
        while True: 
            try: 
                initiateAnswer = sock.recv(1024)
                print("received from server")
                incomingQueue.append(initiateAnswer)
                print(len(incomingQueue))
            except KeyboardInterrupt:
                print("Logging off")
                convo.status.online = False
                convo.status.reply = "Logging off"
                sock.send(pickle.dumps(convo.status))
                quit()
            except:
                print("Error occured during connecting to server")
                exit()

    def processing():
        print("Processing thread open")
        while True:
            time.sleep(0.3) #Waiting a short time to avoid constantly accessing the queue
            if len(incomingQueue) > 0:
                #Popping first in queue, pickle loads it into an object, 
                mes = pickle.loads(incomingQueue.pop(0))
                print('line 77')
                
                #Prints the message:
                print(mes.botName + ": \t" + mes.reply)
                
                # Use that to initiate a reply from the bot, unless this is the one where a user can input. 
                if not convo.status.whichBot < 1:
                    toSend = convo.conversation(mes)

                    #Conversation returns True if it wants something to be sent. 
                    if toSend:
                        sock.send(pickle.dumps(convo.status))
                
                #Checking if convo online status has been set to False, and logging the client off if it has.
                if not convo.status.online:
                    exit() #Throws a keyInterupt error #####################################################################
                    
    def replying(): 
        while True:
            convo.status.reply = input()
            if convo.status.reply == "Exit":
                convo.status.online = False
            sock.send(pickle.dumps(convo.status))

    threadReceive = threading.Thread(target=receive, args=())
    threadSending = threading.Thread(target=processing, args=())

    if convo.status.whichBot == 0:
        threadReply = threading.Thread(target=replying, args=())
        print("You can now write to the bots:")
        threadReply.start()

    threadReceive.start()
    threadSending.start()
    
    if convo.status.whichBot == 0:
        threadReply.join()
    threadReceive.join()
    threadSending.join()
