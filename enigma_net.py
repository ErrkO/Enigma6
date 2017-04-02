from socket import *	  #for establishing a network connection
from Queue import Queue	  #Used as an inbox
import threading          #Used to readincoming traffic and store it in the inbox queue
import thread			  #used to read messages from inbox

#Python 2 doesn't support Enums.
"""When creating an EnigmaNetwork object, it must
	be specified whether it will run as a server or 
	a client"""
class SocketType:
	SERVER = 1	#If running as a server, pass in 'SocketType.SERVER'
	CLIENT = 2	#If running as a client, pass in 'SocketType.CLIENT'

lock = threading.Lock() #used to safely access resources shared my multiple threads
	
	
class EnigmaNet (threading.Thread):
	'Network class for the enigma machine project'
	
	
	#initializes an EnigmaNet object
	#PARAMS:
	#		socket_type: the type of socket, whether it be a server or client socket
	#		address: the IP address to use with the socket. if server, use 0.0.0.0
	#		port: the port number to use with the socket
	#PRECONDITIONS:
	#		socket_type must be either a 1 for server socket, or a 2 for client socket
	#		address must be a string
	#		port must be an int
	#RETURNS:
	#		nothing
	def __init__(self, socket_type, address, port):
		if socket_type != 1 and socket_type != 2:		#testing whether a valid socket_type was passed in
			raise ValueError("Invalid Socket Type")
		if type(address) is not str:					#testing if address is a string
			raise TypeError("address must be a string") 
		if type(port) is not int:						#testing if port is an int
			raise TypeError("port must be an int")
		threading.Thread.__init__(self)					#calling base class constructor
		self.socket_type = socket_type					#setting the socket type	
		self.inbox = Queue()							#initializing inbox queue
		self.address = address							#saving the address
		self.port = port								#saving the port
		self.close_connection = False					#set this to true to terminate conversation
		self.connection_established = False				#gets set to true when a connection is made
	
	
	#puts a message in the outbox. The other thread will handle it.
	#PARAMS:
	#		message: the message to send
	#PRECONDITIONS:
	#		message must not be null, and must be a string
	def send_message(self, message):
		if message is None or type(message) is not str:				
			raise ValueError("message must be a non-null string")
		#sending a message is different depending on whether it is a server socket or a client socket
		if self.socket_type == 2:			
			self.sock.send(message)									
		else:
			self.c.send(message)									
	
	#Will return the oldest message in the inbox, or nothing if there are no messages
	def recieve_message(self):
		if not self.inbox.empty():
			return self.access_inbox(self.inbox.get)
	
	#call this method to close the socket and stop the thread.
	def disconnect(self):
		self.close_connection = True
	
	#will return true if there is a message in the inbox, false otherwise
	def have_mail(self):
		return not self.inbox.empty()
	
	#private helpers
	#------------------------------------------------------------------------------------
	#this method gets called after you call <instance>.start()
	#starts the thread which initializes either a client or server socket
	def run(self):
		if self.socket_type == SocketType.SERVER: #start server socket
			self.__start_server()
		else: 									  #start client socket
			self.__start_client()
	
	
	#creates a server socket.
	def __start_server(self):
		self.sock = socket()					          #creating the socket
		self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #needed to prevent errors that may happen when binding to a recently used port
		self.sock.bind((self.address, self.port))         #binding it the the address and port
		self.sock.listen(1)						 	      #listening for 1 connection
		c, addr = self.sock.accept()			          #establishing connection with client
		self.c = c
		print "connection established"
		self.connection_established = True
		while not self.close_connection:
			message = c.recv(1024)					  	  #if recv doesn't return anything, an exception will be raised
			self.access_inbox(self.inbox.put, message)	  #puts a message into the inbox, gets skipped if exception gets called
			if message == '':							  #if recv ever recieves zero bytes, the connection was broken
				self.close_connection = True
				break;
		self.sock.close()
		
	
	#starts a client socket and attempts to connect to a server socket
	def __start_client(self):
		self.sock = socket()					          #creating the socket
		self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #needed to prevent errors that may happen when binding to a recently used port
		self.sock.connect((self.address, self.port))	  #attempting to connect 
		print "connection established"
		self.connection_established = True
		while not self.close_connection:
			message = self.sock.recv(1024)			 	  #the thread will stall here and wait for data	
			self.access_inbox(self.inbox.put, message)    #puts a message into the inbox, gets skipped if exception gets called
			if message == '':							  #if recv ever recieves zero bytes, the connection was broken
				self.close_connection = True
				break;
		self.sock.close()
		
	
	#this method is meant to either put a message into the inbox queue, or get a message out of the inbox queue
	#because inbox is a shared resource between threads, it had to be more complicated than I would have liked.
	#PARAMS 
	#	message(optional): the message to put into the queue
	#	function: a function pointer. pass in either Queue.gets, or Queue.puts
	def access_inbox(self, function, message = 0):
		accessed = False					#set accessed to false, that way it will loop until it is able to gain access
		while not accessed:
			lock.acquire()					#lock this part so only one thread can use it
			if message == 0:	
				message = function()	
			else:
				function(message)
			accessed = True					#set accessed to true
			lock.release()					#release it so the other thread can use it
		return message

#end class
		

#******************TESTING***************************
#if you want to test this on two seperate computers, change host to '0.0.0.0' on the machine that
#you want to be the server, and change host to '<server's IP>' on the client machine.
host = 'localhost' 
port = 5000
socktype = int(raw_input("enter sock type 1:server, 2:client: "))
en = EnigmaNet(socktype, host, port)
en.start()

def readInbox(threadName, delay):
	while True:
		if en.have_mail():
			print en.recieve_message()

thread.start_new_thread(readInbox, ("ThreadyMcThreadFace", 10))

input = ''
while not input == '-1':
	input = raw_input()
	en.send_message(input)
en.disconnect()