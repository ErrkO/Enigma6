"""Imports"""
from tkinter import * #GUI calls
from tkinter import messagebox

from Mbox import *

#from enigma import * #Enigma Encryption Code
#from enigma_net import * #Enigma networking code

rotorNum = 0
rotorPos = []

"""" Function Section"""
def InitRotorPos():
	global rotorPos
	for i in range(0,rotorNum):
		rotorPos.append(0)

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
	okbttn.pack(pady=15)
	
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

def Rotor_Num():
	popout = Tk()
	popout.title("Rotor Order")
	#popout.geometry("400x100+30+30")
	popout.config(bg="black")
	
	num = StringVar()
	
	Label(popout,text="How many Rotors are there? ",
			bg="black",
			fg="lime",
			font="times 12").grid(row=0,column=0)
			
	e = Entry(popout)
	
	#e1.bind("<Return>",SetRNum)
	
	setbttn = Button(popout,text="Set",command=(lambda: SetRNum(e.get(),closebttn)),
					bg="black",
					fg="lime")
	setbttn.grid(row=0,column=3)
	
	closebttn = Button(popout,text="Close",command=(lambda: popout.destroy()),
					bg="black",
					fg="lime",
					state=DISABLED)
	closebttn.grid(row=2,column=1)
	
	e.grid(row=0,column=1)
	
def ClearScreen(frame):
	for widget in frame.winfo_children():
		widget.destroy()
	
def SetRNum(val,button):
	global rotorNum
	rotorNum = int(val)
	if (rotorNum > 0):
		button['state']='normal'
	else:
		button['state']='disabled'
		Popout("Error","Must have more than zero rotors")
	
def PrintRNum():
	print(val)

def Rotor_Order():
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
	
	printbttn = Button(popout,text="Print",command=(lambda: PrintRotorOrder(entries)),
					bg="black",
					fg="lime")
	printbttn.grid(row=rotorNum+1,column=1+1)
	
	closebttn = Button(popout,text="Close",command=(lambda: popout.destroy()),
					bg="black",
					fg="lime",
					state=DISABLED)
	closebttn.grid(row=rotorNum+2,column=1)
	
def SetRotorOrder(entries,button):
	global rotorPos
	i = 0
	
	InitRotorPos()
	setting = []
	for entry in entries:
		setting.append(int(entry.get()))
		i += 1
		
	for i in range(0,rotorNum):
		rotorPos[i]=setting[i]
		
	if CheckForDuplicate(rotorPos) == True:
		button['state']='disabled'
		Popout("Error","You have duplicate rotor settings")
	elif CheckForDuplicate(rotorPos) == False:
		button['state']='normal'
	
def PrintRotorOrder(entries):
	#InitRotorPos()
	for entry in entries:
		print("Input rotor {0}".format(int(entry.get())))
		rotorPos.append(int(entry.get()))
		
	for i in range(0,rotorNum):
		print("Output rotor {0}".format(rotorPos[i]))
	
def CheckForDuplicate(rotorPos):
	for i in range(0,rotorNum):
		for j in range(0,rotorNum):
			if (rotorPos[i]==rotorPos[j] and i != j):
				return True
				break
			
			# elif(rotorPos[i]==rotorPos[j]):
				# return True
				# break
				
	return False

def Rotor_Setting():
	print(2)
				
def Plug_Board():
	print(3)
	
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
menu.add_cascade(label="Set",menu=setmenu)
setmenu.add_command(label="Rotor Number", command=Rotor_Num)
setmenu.add_command(label="Rotor Order", command=Rotor_Order)
setmenu.add_command(label="Rotor Setting", command=Rotor_Setting)
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



mainloop()