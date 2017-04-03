#******************TESTING***************************
#This file is for testing the enigma_net class
from enigma_net import *
import _thread                      #used to read messages from inbox


#if you want to test this on two seperate computers, change host to '0.0.0.0' on the machine that
#you want to be the server, and change host to '<server's IP>' on the client machine.

#To test the EnigmaNet class on one machine, just set the host variable to 'localhost' and
#run the application twice
host = 'localhost' #the address or hostname of the system you want to connect to.
port = 5555        #the port number you want to use
socktype = int(input("enter sock type 1:server, 2:client: "))
en = EnigmaNet(socktype, host, port)

"""a seperate thread will begin running after calling en.start(). 
    It will read messages in from the socket and place
    those messages in an inbox"""
en.start() 


user_input = ''
"""I'm using a seperate thread to read the messages in from the inbox.
    You don't have to do it this way if you don't want to."""
def readInbox(threadName, delay):
    while True:
        if en.have_mail(): 	            #check if there is a message in the inbox
            print (en.recieve_message())#get the message from the inbox and print it
    if user_input == '-1':
        _thread.exit()
_thread.start_new_thread(readInbox, ("ThreadyMcThreadFace", 10))

#getting user input and sending it. the loop will stop if -1 is entered.
while not user_input == '-1':
    user_input = input()
    if user_input == '-1': break
    en.send_message(user_input) #send the message
    
    
en.disconnect() #disconnect from the network.