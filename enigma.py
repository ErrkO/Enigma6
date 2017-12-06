#!/usr/bin/env python3

import copy
class Enigma:       #Define Enigma Class


    rotors = [ [3, 15, 20, 22, 20, 12, 24, 6, 4, 18, 11, 7, 19, 10, 1, 11, 16, 20, 15, 15, 8, 24, 14, 23, 16, 10],
           [9, 14, 8, 16, 24, 18, 23, 7, 13, 24, 6, 1, 12, 17, 3, 19, 4, 14, 7, 18, 2, 11, 22, 3, 15, 2],
           [16, 24, 12, 14, 11, 13, 20, 12, 5, 3, 17, 9, 16, 24, 7, 14, 20, 5, 12, 16, 3, 10, 12, 1, 8, 8]]
    rotorsRev = [[0 for i in range(26)],[0 for i in range(26)],[0 for i in range(26)]]
    plugboard = [i for i in range(26)]
    checkSwap = [0 for i in range(26)]
    tick = [ 0, 0, 0]
    slot = [-1, -1, -1]
    rotorPosition = [0,0,0]
    rotorSafe = copy.deepcopy(rotors)
    rotorsRevSafe = copy.deepcopy(rotorsRev)
    plugboardSafe = copy.deepcopy(plugboard)
    tickSafe = copy.deepcopy(tick)
    slotSafe = copy.deepcopy(slot)
    rotorPositionSafe = copy.deepcopy(rotorPosition)
    keyArray = [0]
    codeArray = [0]
    codeLength = 0
    textArray = [0]
    newText = " "

    # Constructor Function
    def __init__(self):
        for i in range(0, 3):
            for j in range(0, 26):
                self.rotorsRev[i][(j + (self.rotors[i][j])) % 26] = 26 - (self.rotors[i][j])

    # Function resets Enigma: Does NOT change the key.
    def resetEnigma(self):
        self.rotors = copy.deepcopy(self.rotorSafe)
        self.rotorsRev = copy.deepcopy(self.rotorsRevSafe)
        for i in range(0, 3):
            for j in range(0, 26):
                self.rotorsRev[i][(j + (self.rotors[i][j])) % 26] = 26 - (self.rotors[i][j])
        self.rotorPosition = copy.deepcopy(self.rotorPositionSafe)
        self.tick = copy.deepcopy(self.tickSafe)
        self.plugboard = copy.deepcopy(self.plugboardSafe)
        self.slot = copy.deepcopy(self.slotSafe)
        self.Enigma_setup()
        return


    # Function that establishes the order of the rotors for encryption
    def rotor_Order(self, a, b, c):
        self.slot[0] = a
        self.slot[1] = b
        self.slot[2] = c
        return

    # Function that places the rotors and the reverse rotors at their beginning positions
    def set_rotorPosition(self):
        for i in range(0, 3):
            temp1 = self.rotors[self.slot[i] - 1][:]
            temp2 = self.rotorsRev[self.slot[i] - 1][:]
            for k in range(0, 26):
                self.rotors[self.slot[i] - 1][k] = temp1[(k + self.tick[i]) % 26]
                self.rotorsRev[self.slot[i] - 1][k] = temp2[(k + self.tick[i]) % 26]
        return

    # Function that turns the rotors and reverse rotor one position
    def rotor_moveOne(self, i):
        temp1 = self.rotors[self.slot[i] - 1][:]
        temp2 = self.rotorsRev[self.slot[i] - 1][:]
        for k in range(0, 26):
            self.rotors[self.slot[i] - 1][k] = temp1[(k + 1) % 26]
            self.rotorsRev[self.slot[i] - 1][k] = temp2[(k + 1) % 26]
        return

    # Function that establishes the beginning position of the rotors and reverse rotors
    def rotor_Set(self, a, b, c):
        self.tick[0] = a
        self.tick[1] = b
        self.tick[2] = c
        self.set_rotorPosition()
        return

    # Function that sets up the plug board
    def plug_board(self, plugs):
        for i in range(0, plugs):
            letterOne = ord(self.keyArray[10 + (2 * i)]) - 97
            letterTwo = ord(self.keyArray[11 + (2 * i)]) - 97
            self.checkSwap[letterOne] = 1
            self.checkSwap[letterTwo] = 1
            temp = self.plugboard[letterOne]
            self.plugboard[letterOne] = self.plugboard[letterTwo]
            self.plugboard[letterTwo] = temp
        return

    # Function that swaps code numbers based on the plugboard settings
    def plugSwap(self, codeIndex):
        self.codeArray[codeIndex] = self.plugboard[self.codeArray[codeIndex]]
        return

    # Function that recodes an incoming letter with the current rotor
    def rotorCoding(self, codeIndex, rotorNum):
        self.codeArray[codeIndex] = (self.codeArray[codeIndex] + self.rotors[self.slot[rotorNum] - 1][self.codeArray[codeIndex]]) % 26
        return

    # Function that recodes an incoming letter with the current rotor in the reverse direction
    def rotorCodingRev(self, codeIndex, rotorNum):
        self.codeArray[codeIndex] = (self.codeArray[codeIndex] + self.rotorsRev[self.slot[rotorNum] - 1][self.codeArray[codeIndex]]) % 26
        return

    # Function Setup Enigma
    def Enigma_setup(self):
        self.rotor_Order(int(self.keyArray[0]), int(self.keyArray[1]), int(self.keyArray[2]))
        rotorP1 = [self.keyArray[3], self.keyArray[4]]
        rotorP2 = [self.keyArray[5], self.keyArray[6]]
        rotorP3 = [self.keyArray[7], self.keyArray[8]]
        rotorP1 = ''.join(rotorP1)
        rotorP2 = ''.join(rotorP2)
        rotorP3 = ''.join(rotorP3)
        self.rotor_Set(int(rotorP1), int(rotorP2), int(rotorP3))
        plugs = int(self.keyArray[9])
        self.plug_board(plugs)
        return

    # Function Encrypt/Decrypt message
    def encrypt_decrypt(self):
        # This is the coding section. It calls the functions of rotors and reverse rotors
        # The encoding/decoding happens for letter in the array

        for m in range(0, self.codeLength):
            # Plugswap happens at the beginning based on the plugboard settings
            self.plugSwap(m)

            # Sends the numbers through all 3 rotors in forward order
            for n in range(0, 3):
                self.rotorCoding(m, n)

            # Simple Caesar shift for the reflector
            self.codeArray[m] = (self.codeArray[m] + 13) % 26

            # Sends the numbers through all 3 rotors in reverse order
            for n in range(2, -1, -1):
                self.rotorCodingRev(m, n)

            # Once the numbers have exited, they go through the plugboard again
            self.plugSwap(m)

            # Increments the first rotor by one after each letter is encoded
            # if the first rotor goes past 25, then the next rotor is incremented by one
            # if not then the range is maxxed to exit the loop
            for p in range(0, 3):
                temp = (self.tick[p] + 1) % 26
                self.rotor_moveOne(p)
                if (temp > self.tick[p]):
                    self.tick[p] = temp
                    p = 3
                else:
                    self.tick[p] = temp
        # Converts the 0-25 numbers into ASCII numbers and then back into characters
        # for the textArray String
        for m in range(0, self.codeLength):
            self.textArray[m] = chr(self.codeArray[m] + 97)
        return

    # Function sets Key Array then sets Enigma Machine
    def setKey(self, keyString):
        self.keyArray = keyString
        self.resetEnigma()
        return

    # Function takes text string and prepares it for encryption/decryption
    def prepareText(self, textString):
        self.textArray = list(textString)
        self.codeLength = len(self.textArray)
        self.codeArray = [0 for i in range(self.codeLength)]
        for i in range(0, self.codeLength):
            self.codeArray[i] = ord(self.textArray[i]) - 97
        self.encrypt_decrypt()
        self.newText = ''.join(self.textArray)
        return
