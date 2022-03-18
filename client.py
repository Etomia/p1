import socket
#import threading
import sys
from bots import *

messagesIn = []

#Getting command line parameters
try:
    host = sys.argv[1]
    port = int(sys.argv[2])
    thisBotIN = sys.argv[3]
except:
    print("Please provide command line paramaters in the following order: host, port, botNumber (1-4)")
    exit()

#Checking if correct bot nr is provided
while (not thisBotIN.isnumeric()) or int(thisBotIN) < 1 or int(thisBotIN) > 4:
    thisBotIN = input("Write only, 1, 2, 3, or 4, to cancel write E: ")

    if thisBotIN == "E" or thisBotIN == "e":
        exit()

#starting new bots object
convo = Bots(int(thisBotIN))

#Connects the socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    #sock.listen()
    #sock.sendall(b"Hello, world")
    #listens for answer:
    while True: 
        try: 
            initiateAnswer = sock.recv(1024)
            print("received from server")
            obj = pickle.loads(initiateAnswer)
            print(obj.reply)
            reply = ""
            #reply = convo.conversation(initiateAnswer)
            #if reply == "":
            print("sending...")
            sock.send(b"Hei")
            print("sent!")
        except KeyboardInterrupt:
            quit()
        except:
            print("Error occured during connecting to server")
            break


# convo.startConvo(thisBot, initiateAnswer)


#print(f"Received {data!r}")