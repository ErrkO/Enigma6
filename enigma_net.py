from socket import *	  #for establishing a network connection
from queue import Queue	  #Used as an inbox
import threading          #Used to readincoming traffic and store it in the inbox queue


"""When creating an EnigmaNetwork object, it must
	be specified whether it will run as a server or 
	a client"""
class SocketType:
	SERVER = 1	#If running as a server, pass in 'SocketType.SERVER'
	CLIENT = 2	#If running as a client, pass in 'SocketType.CLIENT'
	


class EnigmaNet (threading.Thread):
	'Network class for the enigma machine project'
	
	host='localhost'
	port=5250
	
	lock = threading.Lock() #used to safely access resources shared my multiple threads
	
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
		self.address = address							#saving the address
		self.port = port								#saving the port
		self.inbox = Queue()							#initializing inbox queue			
		self.connection_established = False				
	
	
	#puts a message in the outbox. The other thread will handle it.
	#PARAMS:
	#		message: the message to send
	#PRECONDITIONS:
	#		message must not be null, and must be a string
	def send_message(self, message):
		if message is None or type(message) is not str:				
			raise ValueError("message must be a non-null string")
		#sending a message is different depending on whether it is a server socket or a client socket
		if self.connection_established:
			if self.socket_type == 2:			
				self.sock.send(bytes(message, 'UTF-8'))									
			else:
				self.c.send(bytes(message, 'UTF-8'))									
	
	
	#Will return the oldest message in the inbox, or nothing if there are no messages
	#RETURNS: the message at the top of the inbox
	def recieve_message(self):
		if not self.inbox.empty():
			return self.access_inbox(self.inbox.get)
	
	
	#call this method to close the socket and stop the thread.
	def disconnect(self):
		self.connection_established = False
	
	
	#will return true if there is a message in the inbox, false otherwise
	def have_mail(self):
		return not self.inbox.empty()
	
	def Set_Host(newHost):
		host=newHost
		
	def Set_Port(newPort):
		return(1)
	
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
		try:
			self.sock = socket()					          #creating the socket
			self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #needed to prevent errors that may happen when binding to a recently used port
			self.sock.bind((self.address, self.port))         #binding it the the address and port
			self.sock.listen(1)						 	      #listening for 1 connection
			c, addr = self.sock.accept()			          #establishing connection with client
			self.c = c
			print ("connection established")
			self.connection_established = True
		except Exception:
			print("An error occurred when creating the server")
		while self.connection_established:
			try:
				message = c.recv(1024)					  	  #if recv doesn't return anything, an exception will be raised
				if message.decode(encoding="utf-8", errors="strict") == '': #if zero bytes are recieved, the connection was closed by the other user
					self.connection_established = False
					print("The other user has disconnected")
					break;
				self.access_inbox(self.inbox.put, message)    #puts a message into the inbox, gets skipped if exception gets called
			except Exception:
				print("Connection lost")
				self.connection_established = False
		c.close()
		self.c = ''
		
	
	#starts a client socket and attempts to connect to a server socket
	#If a it can't connect to the server socket for whatever reason, an error will occur
	def __start_client(self):
		try:
			self.sock = socket()					          #creating the socket
			self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #needed to prevent errors that may happen when binding to a recently used port
			self.sock.connect((self.address, self.port))	  #attempting to connect 
			print("connection established")
			self.connection_established = True
		except Exception:
			print("an error occurred when trying to connect to the server")
		while self.connection_established:
			try:
				message = self.sock.recv(1024)			 	  #the thread will stall here and wait for data	
				if message.decode(encoding="utf-8", errors="strict") == '': #if zero bytes are recieved, the connection was closed by the other user
					self.connection_established = False
					print("The other user has disconnected")
					break
				self.access_inbox(self.inbox.put, message)    #puts a message into the inbox, gets skipped if exception gets called
			#except socket.timeout:
			#	continue
			except Exception:
				print("Connection lost")
				self.connection_established = False
		self.sock.close()
		
	
	#this method is meant to either put a message into the inbox queue, or get a message out of the inbox queue
	#because inbox is a shared resource between threads, it had to be more complicated than I would have liked.
	#PARAMS 
	#	function: a function pointer. pass in either Queue.gets, or Queue.puts
	#	message(optional): the message to put into the queue
	def access_inbox(self, function, message = 0):
		accessed = False					#set accessed to false, that way it will loop until it is able to gain access
		while not accessed:
			EnigmaNet.lock.acquire()		#thread locked so only one thread can use the inbox at one time
			if message == 0:	
				message = function()	    #a message gets read from the inbox
			else:
				function(message.decode(encoding="utf-8", errors="strict")) # message gets put into the inbox
			accessed = True					#set accessed to true 
			EnigmaNet.lock.release()		#release it so the other thread can use 
		return message