import socket
import threading
import sys
from bots import *

messagesIn = []

#Getting command line parameters
try:
    host = sys.argv[1]
    port = int(sys.argv[2])
    thisBotIN = sys.argv[3]
except:
    print("Please provide command line paramaters in the following order: host port botNumber (1-4)")
    exit()

#Checking if correct bot nr is provided
while (not thisBotIN.isnumeric()) or int(thisBotIN) < 1 or int(thisBotIN) > 4:
    thisBotIN = input("Write only, 1, 2, 3, or 4, to exit write E: ")

    if thisBotIN == "E" or thisBotIN == "e":
        exit()

#starting new bots object
convo = Bots(int(thisBotIN) - 1)

#Creating a queue for everything incoming from server, this is so client can still receive from server if client is working on something else
incomingQueue = []

#Connects the socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    print("Connected to server!")
    #sock.listen()
    #sock.sendall(b"Hello, world")
    #listens for answer:
    initiateAnswer = sock.recv(1024)
    print("received from server")

    obj = pickle.loads(initiateAnswer)
    print(obj.reply)

    print("sending...")
    sendObj = pickle.dumps(convo.status)
    sock.send(sendObj)
    print("sent!")

    acc = sock.recv(1024)
    if acc == b"badBot":
        print("This bot already exists, start again and use a different bot number.")
        exit()
    elif acc == b"goodBot": 
        print("Accepted, this bot is now connected!")

    def receive():         
        while True: 
            try: 
                initiateAnswer = sock.recv(1024)
                print("received from server")
                incomingQueue.append(initiateAnswer)
            except KeyboardInterrupt:
                quit()
            except:
                print("Error occured during connecting to server")
                quit()

    def sending():
        while True:
            if incomingQueue.__len__ > 0:
                toSend = convo.conversation(incomingQueue.pop(0))
                if not toSend == b"0":
                    sock.send(pickle.dump(convo.status))
                    


    threadReceive = threading.Thread(target=receive, args=())
    threadSending = threading.Thread(target=sending, args=())
    threadReceive.start()
    threadSending.start()
# convo.startConvo(thisBot, initiateAnswer)


#print(f"Received {data!r}")