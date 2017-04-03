from tkinter import * #GUI calls
from tkinter import messagebox

#from enigma import * #Enigma Encryption Code
#from enigma_net import * #Enigma networking code

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
	
#Menu For the Application
#Menu Initialization
root = Tk()
root.title("Seal Team 6 Enigma Encryption/Decryption")
root.iconbitmap("./Encrypted.ico")
root.geometry("400x400+30+30")

#setting up the menu system
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)

#setting up the file submenu
filemenu.add_command(label="New Conversation", command=NewFile)
filemenu.add_command(label="Open Conversation...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

#setting up the help submenu
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

#Setting up the Welcome Message
Label(root,
		text="Welcome to the Seal Team 6 enigma project",
		font="times 15 bold").pack()


mainloop()