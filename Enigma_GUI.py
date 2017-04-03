from tkinter import * #GUI calls
from tkinter import messagebox

#from enigma import * #Enigma Encryption Code
#from enigma_net import * #Enigma networking code

def NewFile():
    print("New File!")
	
def OpenFile():
    name = askopenfilename()
    print(name)
	
def About():
    messagebox.showinfo("About","This is The Seal Team 6's Enigma Python Program")
	
#Menu For the Application
root = Tk()
root.title("Enigma 6 Encryption/Decryption")
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New Conversation", command=NewFile)
filemenu.add_command(label="Open Conversation...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

Label(root,
		text="Welcome to the Seal Team 6 enigma project").pack()


mainloop()