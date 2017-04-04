"""Imports"""
from tkinter import * #GUI calls
from tkinter import messagebox

from Mbox import *

#from enigma import * #Enigma Encryption Code
#from enigma_net import * #Enigma networking code

rotorNum = '0'

"""" Function Section"""
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
	popout = Tk()
	mbox = popout
	popout.title(title)
	popout.geometry("400x100+30+30")
	popout.config(bg="black")
	
	Label(popout,text=msg,
			bg="black",
			fg="lime",
			font="times 12").pack(pady=10)
	
	okbttn = Button(popout,text="OK",command=popout.destroy,
					bg="black",
					fg="lime")
	okbttn.pack(pady=15)
	
	popout.mainloop()

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

def Rotor_Order():
	popout = Tk()
	popout.title("Rotor Order")
	#popout.geometry("400x100+30+30")
	popout.config(bg="black")
	
	num = StringVar()
	
	Label(popout,text="How many Rotors are there? ",
			bg="black",
			fg="lime",
			font="times 12").grid(row=0,column=0)
			
	e1 = Entry(popout)
	
	#e1.bind("<Return>",SetRNum)
	
	setbttn = Button(popout,text="Set",command=(lambda: SetRNum()),
					bg="black",
					fg="lime")
	setbttn.grid(row=0,column=3)
	
	printbttn = Button(popout,text="Print",command=(lambda: print(rotorNum)),
					bg="black",
					fg="lime")
	printbttn.grid(row=2,column=1)
	
	e1.grid(row=0,column=1)
	
def SetRNum():
	rotorNum = int(self.Entry.get())
	
#def PrintRNum():
	#print(rotorNum)

def Rotor_Settings():
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
setmenu.add_command(label="Rotor Order", command=Rotor_Order)
setmenu.add_command(label="Rotor Setting", command=Rotor_Settings)
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