"""Imports"""
from tkinter import * #GUI calls
from tkinter import messagebox

from Mbox import *
import string

#from enigma import * #Enigma Encryption Code
#from enigma_net import * #Enigma networking code

"""Globals"""
rotorNum = 0
rotorPos = []
rotorSet = []
plugNum = 0
plugCon = []
#letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
			#"n","o","p","q","r","s","t","u","v","w","x","y","z"]
letters = list(string.ascii_lowercase)
keyString = ""

"""" Function Section"""
# Initializes the rotors to 0 positions
def InitRotorPos():
	global rotorPos
	for i in range(0,rotorNum):
		rotorPos.append(0)

# Initializes the rotor settings to -1
def InitRotorSetting():
	global rotorSet
	for i in range(0,rotorNum):
		rotorSet.append(-1)

# Initializes the plugCon to a space		
def InitPlugCon():
	global plugCon
	for i in range(0,plugNum*2):
		plugCon.append(" ")

def Print(val):
	print(val)
		
def GenerateKeyString():
	global keyString
	
	rostring = ""
	rsstring = ""
	pnstring = str(plugNum)
	pcstring = ""
	
	for i in range(rotorNum):
		rostring += str(rotorPos[i])
		if rotorSet[i] < 10:
			rsstring += str(0) + str(rotorSet[i])
		else:
			rsstring += str(rotorSet[i])
	
	for i in range(plugNum*2):
		pcstring += str(plugCon[i])
		
	return rostring + rsstring + pnstring + pcstring
	
#Function for a new file
def NewFile():
    print("New File!")
	
#Function to open a file
def OpenFile():
    name = askopenfilename()
    print(name)
	
#Function to display the about message
def About():
    messagebox.showinfo("About","This is The Seal Team 6's Enigma Python Program")
	
#Function to display a properly styled message box
def About2():
	Popout("About","This is The Seal Team 6 Enigma Python Program")

# Function to display a simple message box with a configurable title and message
def Popout(title,msg):
	popout1 = Tk()
	popout1.title(title)
	popout1.geometry("400x100+30+30")
	popout1.config(bg="black")
	
	Label(popout1,text=msg,
			bg="black",
			fg="lime",
			font="times 12").pack(pady=10)
	
	okbttn = Button(popout1,text="OK",command=popout1.destroy,
					bg="black",
					fg="lime")
	okbttn.pack(pady=10)
	
	popout1.mainloop()

#Depracated message box
def MboxExample():
	popout = tkinter.Tk()
	mbox = Mbox
	mbox.root = popout
	
	D = {'user':'bob'}
	
	b_login = tkinter.Button(popout, text='Log in')
	b_login['command'] = lambda: Mbox('Name?', (D, 'user'))
	b_login.pack()

	b_loggedin = tkinter.Button(popout, text='Current User')
	b_loggedin['command'] = lambda: Mbox(D['user'])
	b_loggedin.pack()

# GUI Function to retrieve the number of rotors the user desires
def Rotor_Num(var=NONE):
	popout = Tk()
	popout.title("Rotor Order")
	#popout.geometry("400x100+30+30")
	popout.config(bg="black")
	
	Label(popout,text="How many Rotors are there? ",
			bg="black",
			fg="lime",
			font="times 12").grid(row=0,column=0)
			
	e = Entry(popout)
	
	setbttn = Button(popout,text="Set",command=(lambda: SetRNum(e.get(),closebttn)),
					bg="black",
					fg="lime")
	setbttn.grid(row=0,column=3)
	
	if var == NONE:
		closebttn = Button(popout,text="Close",command=(lambda: popout.destroy()),
						bg="black",
						fg="lime",
						state=DISABLED)
		closebttn.grid(row=2,column=1)
		
	else:
		closebttn = Button(popout,text="Next",command=(lambda: Next(popout,Rotor_Order)),
						bg="black",
						fg="lime",
						state=DISABLED)
		closebttn.grid(row=2,column=1)
	
	e.grid(row=0,column=1)

# Simple function to clear the screen	
def ClearScreen(frame):
	for widget in frame.winfo_children():
		widget.destroy()
		
def Next(frame,func):
	frame.destroy()
	func(1)

# Helper function to enable the close button and set the rotor number
def SetRNum(val,button):
	global rotorNum
	rotorNum = int(val)
	if (rotorNum > 0):
		button['state']='normal'
	else:
		button['state']='disabled'
		Popout("Error","Must have more than zero rotors")

# Potentially deprecated Print function
def PrintRNum():
	print(val)

# GUI Function to get the position of all the rotors
def Rotor_Order(var=NONE):
	if rotorNum <= 0:
		Popout("Error","Make sure your rotors are set")
	else:
		popout = Tk()
		popout.title("Rotor Order")
		#popout.geometry("400x100+30+30")
		popout.config(bg="black")
	
		entries = []
		for i in range(0,rotorNum):
			Label(popout,text=("Set the rotor for position {0}: ".format(i+1)),
				bg="black",
				fg="lime",
				font="times 12").grid(row=i,column=0)
			e2 = Entry(popout)
			e2.grid(row=i, column=1)
			entries.append(e2)
		
		setbttn = Button(popout,text="Set",command=(lambda: SetRotorOrder(entries,closebttn)),
						bg="black",
						fg="lime")
		setbttn.grid(row=rotorNum+1,column=1)
	
		if var == NONE:
			closebttn = Button(popout,text="Close",command=(lambda: popout.destroy()),
						bg="black",
						fg="lime",
						state=DISABLED)
			closebttn.grid(row=rotorNum+2,column=1)
			
		else:
			closebttn = Button(popout,text="Next",command=(lambda: Next(popout,Rotor_Setting)),
						bg="black",
						fg="lime",
						state=DISABLED)
			closebttn.grid(row=rotorNum+2,column=1)

# Helper function to enable the button and set the rotor positions
def SetRotorOrder(entries,button):
	global rotorPos
	
	InitRotorPos()
	setting = []
	for entry in entries:
		setting.append(int(entry.get()))
		
	for i in range(0,rotorNum):
		rotorPos[i]=setting[i]
		
	if CheckForDuplicate(rotorPos,rotorNum) == True:
		button['state']='disabled'
		Popout("Error","You have duplicate rotor settings")
	elif CheckForDuplicate(rotorPos,rotorNum) == False:
		button['state']='normal'

# Deprecated print function for testing
def PrintRotorOrder(entries):
	#InitRotorPos()
	for entry in entries:
		print("Input rotor {0}".format(int(entry.get())))
		rotorPos.append(int(entry.get()))
		
	for i in range(0,rotorNum):
		print("Output rotor {0}".format(rotorPos[i]))

# Helper function to check for duplicate rotors in the SetRotorOrder function
def CheckForDuplicate(array,length):
	for i in range(0,length):
		for j in range(0,length):
			if (array[i]==array[j] and i != j):
				return True
				break
			
			# elif(rotorPos[i]==rotorPos[j]):
				# return True
				# break
				
	return False

# GUI Function to get the rotor settings
def Rotor_Setting(var=NONE):
	if rotorNum <= 0:
		Popout("Error","Make sure your rotors are set")
	else:
		popout = Tk()
		popout.title("Rotor Settings")
		#popout.geometry("400x100+30+30")
		popout.config(bg="black")
	
		entries = []
		for i in range(0,rotorNum):
			Label(popout,text=("Enter the setting for rotor {0} <0-26>: ".format(i+1)),
				bg="black",
				fg="lime",
				font="times 12").grid(row=i,column=0)
			e2 = Entry(popout)
			e2.grid(row=i, column=1)
			entries.append(e2)
	
		setbttn = Button(popout,text="Set",command=(lambda: SetRotorSetting(entries,closebttn)),
						bg="black",
						fg="lime")
		setbttn.grid(row=rotorNum+1,column=1)
		
		if var == NONE:
			closebttn = Button(popout,text="Close",command=(lambda: popout.destroy()),
						bg="black",
						fg="lime",
						state=DISABLED)
			closebttn.grid(row=rotorNum+2,column=1)
			
		else:
			closebttn = Button(popout,text="Next",command=(lambda: Next(popout,Plug_Number)),
						bg="black",
						fg="lime",
						state=DISABLED)
			closebttn.grid(row=rotorNum+2,column=1)

# Helper function to set the rotor settings
def SetRotorSetting(entries, button):
	global rotorSet
	InitRotorSetting()
	
	setting = []
	for entry in entries:
		setting.append(int(entry.get()))
	
	for i in range(0,rotorNum):
		rotorSet[i] = setting[i]
		
	if (CheckForOoR(rotorSet) == True):
		button['state']='disabled'
		Popout("Error","You're rotor settings cannot be above 26 or below 0")
	else:
		button['state']='normal'
	
# Function to check the rotor settings for out of range
def CheckForOoR(array):
	for i in range(0,rotorNum):
		if rotorSet[i] < 0 or rotorSet[i] > 26:
			return True
			break
	
	return False

# GUI Function to determine the number of plugs
def Plug_Number(var=NONE):
	popout = Tk()
	popout.title("Rotor Settings")
	#popout.geometry("400x100+30+30")
	popout.config(bg="black")
	
	Label(popout,text="How many Plugs are there? ",
			bg="black",
			fg="lime",
			font="times 12").grid(row=0,column=0)
			
	e = Entry(popout)
	
	setbttn = Button(popout,text="Set",command=(lambda: SetPNum(e.get(),closebttn)),
					bg="black",
					fg="lime")
	setbttn.grid(row=0,column=3)
	
	if var == NONE:
		closebttn = Button(popout,text="Close",command=(lambda: popout.destroy()),
					bg="black",
					fg="lime",
					state=DISABLED)
		closebttn.grid(row=2,column=1)
			
	else:
		closebttn = Button(popout,text="Next",command=(lambda: Next(popout,Plug_Board)),
					bg="black",
					fg="lime",
					state=DISABLED)
		closebttn.grid(row=2,column=1)
	
	e.grid(row=0,column=1)

# Helper function to set the plugNum
def SetPNum(val,button):
	global plugNum
	plugNum = int(val)
	if (plugNum > 0):
		button['state']='normal'
	else:
		button['state']='disabled'
		Popout("Error","Must have more than zero plugs")

# GUI Function to get and set the plug connections
def Plug_Board(var=NONE):
	if plugNum <= 0:
		Popout("Error","Make sure your plugs are set")
	elif plugNum > 0:
		popout = Tk()
		popout.title("Plug Settings")
		#popout.geometry("400x100+30+30")
		popout.config(bg="black")
	
		entries = []
		j = 0
		for i in range(0,plugNum):
			Label(popout,text=("Enter plug connection {0}-{1} <a-z>: ".format(i+1,1)),
					bg="black",
					fg="lime",
					font="times 12").grid(row=j,column=0)
			e2 = Entry(popout)
			e2.grid(row=j, column=1)
			j += 1
			Label(popout,text=("Enter plug connection {0}-{1} <a-z>: ".format(i+1,2)),
					bg="black",
					fg="lime",
					font="times 12").grid(row=j,column=0)
			e3 = Entry(popout)
			e3.grid(row=j, column=1)
			j += 1
			entries.append(e2)
			entries.append(e3)
	
		setbttn = Button(popout,text="Set",command=(lambda: SetPlugSetting(entries,closebttn)),
						bg="black",
						fg="lime")
		setbttn.grid(row=(plugNum*2)+1,column=1)
	
		closebttn = Button(popout,text="Close",command=(lambda: popout.destroy()),
						bg="black",
						fg="lime",
						state=DISABLED)
		closebttn.grid(row=(plugNum*2)+2,column=1)

def SetPlugSetting(entries,button):
	global plugCon
	InitPlugCon()
	
	setting = []
	for entry in entries:
		el = entry.get()
		setting.append(el.lower())
	
	for i in range(0,plugNum*2):
		plugCon[i] = setting[i]
		
	if (CheckForLetter(plugCon) == False or CheckForDuplicate(plugCon,plugNum*2) == True):
		button['state']='disabled'
		Popout("Error","You are only allowed to input letters,\n and letters cannot be duplicate")
	else:
		button['state']='normal'

# Checks to see if the array contains letters
def CheckForLetter(array):	# true means there is a letter false means not a letter
	boolforpos = []
	for i in range(plugNum*2):
		boolforpos.append(False)
	
	for i in range(plugNum*2):
		boolforpos[i] = False
		for j in range(26):
			if array[i] == letters[j]:
				boolforpos[i] = boolforpos[i] or True
				
	alltrue = boolforpos[0]
	
	for i in range(1,(plugNum*2)):
		alltrue = alltrue and boolforpos[i]
		
	return alltrue

def GetIP():
	print(4)
	
"""Menu Section"""	

#Menu For the Application
#Menu Initialization
root = Tk()
root.title("Seal Team 6 Enigma Encryption/Decryption")
root.iconbitmap("./Encrypted.ico")
root.geometry("400x400+30+30")

#setting up the menu system
menu = Menu(root,background='black',foreground='lime',
				activebackground='lime',activeforeground='black')
root.config(menu=menu,bg='black')
filemenu = Menu(menu,background='black',foreground='lime',
				activebackground='lime',activeforeground='black')
menu.add_cascade(label="File", menu=filemenu)

#setting up the file submenu
filemenu.add_command(label="New Conversation", command=NewFile)
filemenu.add_command(label="Open Conversation...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

#Setting the Enigma Menu
setmenu = Menu(menu,background='black',foreground='lime',
				activebackground='lime',activeforeground='black')
menu.add_cascade(label="Change",menu=setmenu)
setmenu.add_command(label="Rotor Number", command=Rotor_Num)
setmenu.add_command(label="Rotor Order", command=Rotor_Order)
setmenu.add_command(label="Rotor Setting", command=Rotor_Setting)
setmenu.add_command(label="Plug Number", command=Plug_Number)
setmenu.add_command(label="Plug Board", command=Plug_Board)

#Networking Menu
networkmenu = Menu(menu,background='black',foreground='lime',
				activebackground='lime',activeforeground='black')
menu.add_cascade(label="Network",menu=networkmenu)
networkmenu.add_command(label="IP Address",command=GetIP)


#setting up the help submenu
helpmenu = Menu(menu,background='black',foreground='lime',
				activebackground='lime',activeforeground='black')
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About2)
helpmenu.add_command(label="Mbox Example", command=MboxExample)

#Setting up the Welcome Message
Label(root,
		text="Welcome to the Seal Team 6 enigma project",
		bg="black",
		fg="lime",
		font="times 15 bold").pack()
		
setbttn = Button(root,text="Set All Settings",command=(lambda: Rotor_Num(1)),
					bg="black",
					fg="lime")
setbttn.pack()

printbttn = Button(root,text="Print Key String",command=(lambda: Print(GenerateKeyString())),
					bg="black",
					fg="lime")
printbttn.pack()



mainloop()