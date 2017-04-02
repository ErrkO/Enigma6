#Function that establishes the order of the rotors for encryption
def rotor_Order(numRotors):
    for i in range(0,numRotors):
        choice = -1
        while(choice!=1 and choice!=2 and choice !=3) or (choice==slot[0] or choice==slot[1] or choice==slot[2]):
            print("Which rotor would you like to put in slot ", i+1," : ")
            choice = int(input())
            if (choice!=1 and choice!=2 and choice !=3):
                print ("That is not a valid rotor. Try again.")
            if (choice == slot[0] or choice == slot[1] or choice == slot[2]):
                print ("That rotor has already been chosen. Try again.")
        slot[i] = choice
        i += 1
    return

#Function that places the rotors and the reverse rotors at their beginning positions
def set_rotorPosition(numRotors):
    for i in range(0,numRotors):
        temp1 = rotors[slot[i]-1][:]
        temp2 = rotorsRev[slot[i] - 1][:]
        for k in range(0,26):
            rotors[slot[i] - 1][k]= temp1[(k + tick[i]) % 26]
            rotorsRev[slot[i] - 1][k] = temp2[(k + tick[i]) % 26]
        print(rotors[slot[i]-1][:])
    return

#Function that turns the rotos and reverse rotor one position
def rotor_moveOne(i):
    temp1 = rotors[slot[i] - 1][:]
    temp2 = rotorsRev[slot[i] - 1][:]
    for k in range(0,26):
        rotors[slot[i] - 1][k]= temp1[(k + 1) % 26]
        rotorsRev[slot[i] - 1][k] = temp2[(k + 1) % 26]
    print(rotors[slot[i]-1][:])
    return

#Function that establishes the beginning position of the rotors and reverse rotors
def rotor_Set(numRotors):
    for i in range(0,numRotors):
        choice = -1
        print("Set rotor ", i+1, " (between 0-25)")
        while((choice > 25) or (choice < 0)):
            choice = int(input())
            if ((choice > 25) or (choice < 0)):
                print ("That is not a valid choice for a rotor setting. Choose (0-25)")
        tick[i] = choice
    set_rotorPosition(numRotors)
    return

#Function that sets up the plug board
def plug_board():
    plugs = -1
    print('')
    print('How many plugs do you want to attach?')
    while ((plugs<0) or (plugs>13)):
        plugs = int(input())
        if ((plugs<0) or (plugs>13)):
            print ('Too many or too few plugs. Try again.')
    for i in range(0, plugs):
        print('Which two letters to connect with plug ', i+1)
        letterOne = -1
        letterTwo = -1
        while (letterOne<0 or letterOne>25 or letterTwo<0 or letterTwo>25 or letterOne==letterTwo):
            letterOne = ord(input()) - 97
            letterTwo = ord(input()) - 97
            if (letterOne<0 or letterOne>25 or letterTwo<0 or letterTwo>25):
                print('One of the letters is out of bounds. Try again.')
            if (checkSwap[letterOne]==1 or checkSwap[letterTwo]==1):
                print('That letter already has a plug in it. Try a different pair.')
                letterOne = -1
        checkSwap[letterOne] = 1
        checkSwap[letterTwo] = 1
        temp = plugboard[letterOne]
        plugboard[letterOne] = plugboard[letterTwo]
        plugboard[letterTwo] = temp
    print (plugboard)

#Function that swaps code numbers based on the plugboard settings
def plugSwap(codeIndex):
    codeArray[codeIndex] = plugboard[codeArray[codeIndex]]
    return

#Function that recodes an incoming letter with the current rotor
def rotorCoding(codeIndex, rotorNum):
    codeArray[codeIndex] = (codeArray[codeIndex] + rotors[slot[rotorNum]-1][codeArray[codeIndex]])%26
    return

#Function that recodes an incoming letter with the current rotor in the reverse direction
def rotorCodingRev(codeIndex, rotorNum):
    codeArray[codeIndex] = (codeArray[codeIndex] + rotorsRev[slot[rotorNum]-1][codeArray[codeIndex]])%26
    return


#The hard coded setting of the ZERO position of the three rotors
rotors = [ [3, 15, 20, 22, 20, 12, 24, 6, 4, 18, 11, 7, 19, 10, 1, 11, 16, 20, 15, 15, 8, 24, 14, 23, 16, 10],
           [9, 14, 8, 16, 24, 18, 23, 7, 13, 24, 6, 1, 12, 17, 3, 19, 4, 14, 7, 18, 2, 11, 22, 3, 15, 2],
           [16, 24, 12, 14, 11, 13, 20, 12, 5, 3, 17, 9, 16, 24, 7, 14, 20, 5, 12, 16, 3, 10, 12, 1, 8, 8]]
rotorsRev = [ [0 for i in range(26)],[0 for i in range(26)],[0 for i in range(26)]]
plugboard = [i for i in range(26)]
checkSwap = [0 for i in range(26)]
tick = [ 0, 0, 0]
slot = [-1, -1, -1]
rotorPosition = [0,0,0]

#Loop sets up the reverse coded setting of the three rotors
for i in range(0,3):
    for j in range(0,26):
        rotorsRev[i][(j + (rotors[i][j]))%26] = 26-(rotors[i][j])

#Intro to set up the Enigma Machine
print ("Welcome to Seal Team 6 Enigma! You need to set up the Enigma for encryption/decryption.")
print ('')
print ('First, decide the order of the rotors.')
rotor_Order(3)

print ('Now, decide what setting each rotor has.')
rotor_Set(3)

print ('Next, you need to attach the plug board.')
plug_board()

#Enter text to be encrypted or decrypted
print ('Enter text to be encrypted/decrypted (lowercase letters only) -')
someText = input()

#This converts a string into a character array
textArray = list(someText)

#Converts the string array into an (ASCII array - 97)
#Since 'a' = ASCII 97, this converts all characters into numbers
#of the range 0-25
#These numbers are used for encoding/decoding during this section of the program
codeLength = len(textArray)
codeArray = [0 for i in range(codeLength)]
for i in range(0,codeLength):
    codeArray[i] = ord(textArray[i])-97

#This is the coding section. It calls the functions of rotors and reverse rotors
#The encoding/decoding happens for letter in the array
for m in range(0, codeLength):
    #Plugswap happens at the beginning based on the plugboard settings
    plugSwap(m)

    #Sends the numbers through all 3 rotors in forward order
    for n in range(0,3):
        rotorCoding(m,n)

    #Simple Caesar shift for the reflector
    codeArray[m] = (codeArray[m] + 13)%26

    #Sends the numbers through all 3 rotors in reverse order
    for n in range(2,-1,-1):
        rotorCodingRev(m,n)

    #Once the numbers have exited, they go through the plugboard again
    plugSwap(m)

    #Increments the first rotor by one after each letter is encoded
    # if the first rotor goes past 25, then the next rotor is incremented by one
    # if not then the range is maxxed to exit the loop
    for p in range (0,3):
        temp = (tick[p] + 1)%26
        rotor_moveOne(p)
        if (temp > tick[p]):
            tick[p] = temp
            p = 3
        else:
            tick[p] = temp

#Converts the 0-25 numbers into ASCII numbers and then back into characters
# for the textArray String
for m in range(0, codeLength):
    textArray[m] = chr(codeArray[m]+97)

#Converts a character array back into a string
newText = ''.join(textArray)

#Prints out the encoded/decoded text
print(newText)
















