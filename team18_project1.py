#@Authors - Gese Rocha, Andrew Gonzalez
import sys


# Masks for shifting
specialMask = 0x1FFFFF

rnMask = 0x3E0  # 1st argument ARM Rn
rmMask = 0x1F0000  # second argument ARM rm
rdMask = 0x1F  # destination ARM Rd
imMask = 0x3FFC00  # ARM I Immediate
shmtMask = 0xFC00  # ARM ShAMT
addrMask = 0x1FF000  # ARM address for ld and st
addr2Mask = 0xFFFFE0  # addr for CB format
addr3Mask = 0x3FFFFFF # addr for B format
imsftMask = 0x600000  # shift for IM format
imdataMask = 0x1FFFE0  # data for IM type
# last5Mask = 0x7C0
tagMask = 4294967264  # tag for cache
setMask = 24 # set for cache


# containers for instructions
opcodeStr = []
instrSpaced = []
arg1 = []
arg2 = []
arg3 = []
arg1Str = []
arg2Str = []
arg3Str = []
data = []
bindata = []
opcode = []
mempc = []
reg = []
instructionString = []

# containers for simulator
reg = [0] * 32
    # containers for cache
cacheSets = [[[0,0,0,0,0],[0,0,0,0,0]],
             [[0,0,0,0,0],[0,0,0,0,0]],
             [[0,0,0,0,0],[0,0,0,0,0]],
             [[0,0,0,0,0],[0,0,0,0,0]]]
justMissedList = []
lruBit = [0,0,0,0]

preIssueBuff = [-1,-1,-1,-1] # list of 4 instr indexes
preAluBuff = [-1,-1] # 1st is instr index, 2nd is instr index
preMemBuff = [-1,-1]

postAluBuff = [-1,-1] #1st number is value, 2nd is instr index
postMemBuff = [-1,-1]

dest = []
src1 = []
src2 = []
fetchPC = 96
dataSwitch = True #use to determine if instruction or data are being fetched
clearCounter = 0

#file names
outputFileName = ''
inputFileName = ''

inputFileName = 'R_type_test.txt'
outputFileName = 'R_type_test_output'

instructions = [line.rstrip() for line in open(inputFileName, 'rb')]


def bin2StrSpacedRandR(s):
    spacedStr = s[0:11] + " " + s[11:16] + " " + s[16:22] + " " + s[22:27] + " " + s[27:32]
    return spacedStr


def bin2StrSpacedRandD(s):
    spacedStr = s[0:11] + " " + s[11:20] + " " + s[20:22] + " " + s[22:27] + " " + s[27:32]
    return spacedStr


def bin2StringSpaced(s):
    spacedstr = s[0:8] + " " + s[8:11] + " " + s[11:16] + " " + s[16:21] + " " + s[21:26] + " " + s[26:32]
    return spacedstr


def bin2StringSpacedB(s):
    spacedStr = s[0:6] + " " + s[6:32]
    return spacedStr


def bin2StringSpacedI(s):
    spacedStr = s[0:10] + " " + s[10:22] + " " + s[22:27] + " " + s[27:32]
    return spacedStr


def bin2StringSpacedCB(s):
    spacedStr = s[0:8] + " " + s[8:27] + " " + s[27:32]
    return spacedStr


def bin2StringSpacedIM(s):
    spacedStr = s[0:9] + " " + s[9:11] + " " + s[11:27] + " " + s[27:32]
    return spacedStr


def immBitTo32BitConverter(num, bitsize):

    if bitsize == 19:
        negBitMask = 0x40000
        negExtendMask = 0xFFF80000
        negbit = (num & negBitMask) >> 18

        if negbit == 1:
            return (num ^ negExtendMask)
        else:
            return num
    elif bitsize == 26:
        negBitMask = 0x2000000
        negExtendMask = 0xFC000000
        negbit = (num & negBitMask) >> 25

        if negbit == 1:
            return (num ^ negExtendMask)
        else:
            return num


def imm32Bit2ComplementToDec(num):
    flipBitsMak = 0xFFFFFFFF

    signBitMask = 0x80000000

    if (num & signBitMask) >> 31:
        return -((num-1) ^ flipBitsMak)
    else:
        return num


def imm32BitUnsignedTo32BitSignedConverter(s):
    spacedStr = s[0:32] & specialMask
    return spacedStr

class Dissasembler:

    # def __init__(self):


    def run(self):
        global opcodeStr
        global instrSpaced
        global arg1
        global arg2
        global arg3
        global arg1Str
        global arg2Str
        global arg3Str
        global opcode
        global mempc
        global instructionString
        global inputFileName
        global outputFileName

        pc = 0

        # for i in range(len(sys.argv)):
        #     if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
        #         inputFileName = sys.argv[i + 1]
        #         print(inputFileName)
        #     elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
        #         outputFileName = sys.argv[i + 1]

        # This is for testing only
        

        # Translating instructions
        for i in range(len(instructions)):
            opcode.append(int(instructions[i][0:11], 2))

            # This section is for R format instructions
            if opcode[i] == 1112:

                opcodeStr.append("ADD")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", R" + str(arg2[i]))
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StrSpacedRandR(instructions[i]))
                mempc.append(96 + (pc*4))

            elif opcode[i] == 1624:

                opcodeStr.append("SUB")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", R" + str(arg2[i]))
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StrSpacedRandR(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif opcode[i] == 1104:
                opcodeStr.append("AND")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", R" + str(arg2[i]))
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StrSpacedRandR(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif opcode[i] == 1360:
                opcodeStr.append("ORR")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", R" + str(arg2[i]))
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StrSpacedRandR(instructions[i]))
                mempc.append(96 + (pc * 4))

            # This section is for I instructions
            elif 1160 <= opcode[i] <= 1161:
                opcodeStr.append("ADDI")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & imMask) >> 10)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", #" + str(arg2[i]))
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StringSpacedI(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif 1672 <= opcode[i] <= 1673:
                opcodeStr.append("SUBI")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & imMask) >> 10)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", #" + str(arg2[i]))
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StringSpacedI(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif opcode[i] == 1984:
                opcodeStr.append("STUR")
                arg1.append((int(instructions[i], base=2) & rdMask) >> 0)
                arg2.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg3.append((int(instructions[i], base=2) & addrMask) >> 12)
                dest.append(arg2[i])
                src1.append(arg1[i])
                src2.append(arg3[i])
                arg1Str.append("\tR" + str(arg1[i]))
                arg2Str.append(", [R" + str(arg2[i]))
                arg3Str.append(", #" + str(arg3[i]) + "]")
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StrSpacedRandD(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif opcode[i] == 1986:
                opcodeStr.append("LDUR")
                arg1.append((int(instructions[i], base=2) & rdMask) >> 0)
                arg2.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg3.append((int(instructions[i], base=2) & addrMask) >> 12)
                dest.append(arg1[i])
                src1.append(arg2[i])
                src2.append(arg3[i])
                arg1Str.append("\tR" + str(arg1[i]))
                arg2Str.append(", [R" + str(arg2[i]))
                arg3Str.append(", #" + str(arg3[i]) + "]")
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StrSpacedRandD(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif opcode[i] == 0:
                opcodeStr.append("NOP")
                arg1.append(0)
                arg2.append(0)
                arg3.append(0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append("")
                arg2Str.append("")
                arg3Str.append("")
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StringSpaced(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif opcode[i] == 1690:
                opcodeStr.append("LSR")
                arg1.append((int(instructions[i], base=2) & shmtMask) >> 10)
                arg2.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg2[i])
                src2.append(arg1[i])
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg2[i]))
                arg3Str.append(", #" + str(arg1[i]))
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StrSpacedRandD(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif opcode[i] == 1691:
                opcodeStr.append("LSL")
                arg1.append((int(instructions[i], base=2) & shmtMask) >> 10)
                arg2.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg2[i])
                src2.append(arg1[i])
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg2[i]))
                arg3Str.append(", #" + str(arg1[i]))
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StrSpacedRandD(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif 160 <= opcode[i] <= 191:
                opcodeStr.append("B")
                arg1.append(imm32Bit2ComplementToDec(immBitTo32BitConverter(int(instructions[i], base=2) & addr3Mask, 26)))
                arg2.append(0)
                arg3.append(0)
                dest.append(arg1[i])
                src1.append(arg2[i])
                src2.append(arg3[i])
                arg1Str.append("\t#" + str(arg1[i]))
                arg2Str.append('')
                arg3Str.append('')
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StringSpacedB(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif 1440 <= opcode[i] <= 1447:
                opcodeStr.append("CBZ")
                arg1.append(imm32Bit2ComplementToDec(immBitTo32BitConverter(((int(instructions[i], base=2) & addr2Mask) >> 5), 19)))
                arg2.append((int(instructions[i], base=2) & rdMask) >> 0)
                arg3.append(0)
                dest.append(arg2[i])
                src1.append(arg1[i])
                src2.append(arg3[i])
                arg1Str.append("\tR" + str(arg2[i]))
                arg2Str.append(", #" + str(arg1[i]))
                arg3Str.append("")
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StringSpacedCB(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif 1448 <= opcode[i] <= 1455:
                opcodeStr.append("CBNZ")
                arg3.append(0)
                arg1.append(imm32Bit2ComplementToDec(immBitTo32BitConverter((int(instructions[i], base=2) & addr2Mask) >> 5, 19)))
                arg2.append((int(instructions[i], base=2) & rdMask) >> 0)
                dest.append(arg2[i])
                src1.append(arg1[i])
                src2.append(arg3[i])
                arg1Str.append("\tR" + str(arg2[i]))
                arg2Str.append(", #" + str(arg1[i]))
                arg3Str.append("")
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StringSpacedCB(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif 1684 <= opcode[i] <= 1687:

                opcodeStr.append("MOVZ")
                arg1.append((int(instructions[i], base=2) & imsftMask) >> 21)
                arg2.append((int(instructions[i], base=2) & imdataMask) >> 5)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg2[i])
                src2.append(arg1[i])
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", " + str(arg2[i]))
                arg3Str.append(", LSL " + str(arg1[i]*16))
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StringSpacedIM(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif 1940 <= opcode[i] <= 1943:
                opcodeStr.append("MOVZK")
                arg1.append((int(instructions[i], base=2) & imsftMask) >> 21)
                arg2.append((int(instructions[i], base=2) & imdataMask) >> 5)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg2[i])
                src2.append(arg1[i])
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", " + str(arg2[i]))
                arg3Str.append(", LSL " + str(arg1[i]*16))
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StringSpacedIM(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif opcode[i] == 1872:
                opcodeStr.append("EOR")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", R" + str(arg2[i]))
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StrSpacedRandR(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif opcode[i] == 1692:
                opcodeStr.append("ASR")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & shmtMask) >> 10)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", #" + str(arg2[i]))
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StrSpacedRandR(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif opcode[i] == 2038:
                opcodeStr.append("BREAK")
                arg1.append(0)
                arg2.append(0)
                arg3.append(0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append("")
                arg2Str.append("")
                arg3Str.append("")
                instructionString.append(opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i])
                instrSpaced.append(bin2StringSpaced(instructions[i]))
                mempc.append(96 + (pc * 4))
                pc += 1
                break

            pc += 1

        for i in range(pc, len(instructions)):
            bindata.append(instructions[i])
            data.append(imm32Bit2ComplementToDec(int(instructions[i], base=2)))
            mempc.append(96 + (pc * 4))
            pc += 1

        with open(outputFileName + "_dis.txt", 'w') as f:
            for i in range(len(mempc) - len(data)):
                f.write((instrSpaced)[i])
                f.write("\t"+str(mempc[i])+"\t")
                f.write(instructionString[i])
                f.write("\n")

            for i in range(len(data)):
                f.write(bindata[i])
                f.write("\t" + str(mempc[(len(mempc) - len(data)) + i]))
                f.write("\t" + str(data[i]))
                f.write("\n")



dissme = Dissasembler()
dissme.run()


# Helper function to find address
def getIndexOfMemAddress(address, numInstructions):

    # gets index from mempc
    try:
        index = mempc.index(address)
    except ValueError:
        return -1
    
    # if instruction then index is the same
    if index < numInstructions:
        return index
    # if data then index is align for data list
    else:
        return index - numInstructions


# Input changes based on what is being passed in. If instruction then mem index is set to -1, vice versa. Other two are for Writing to mem(STUR Instruction)
def accessMem(memIndex, instructionIndex, isWriteToMem, dataToWrite):

    numInstructions = len(opcode)

    # Dealing with an instruction so we find the relative address of the intrucions
    if(memIndex == -1):
        addressLocal = 96 + (4 * instructionIndex)
    # Dealing with Data so we find the relative address of the Data 
    else:
        addressLocal = 96 + (4 * numInstructions) + (4 * memIndex)

    # Getting the address for both words
    if addressLocal % 8 == 0:
        dataWord = 0 # block 0 was the address
        address1 = addressLocal
        address2 = addressLocal + 4
    if addressLocal % 8 != 0:
        dataWord = 0 # block 1 was the address
        address1 = addressLocal - 4
        address2 = addressLocal
    
    # Getting data for both words
        # Word 0
    if address1 < 96 + (4 * numInstructions): # For Instruction
        data1 = instructions[getIndexOfMemAddress(address1, numInstructions)]
    else: # For Data
        data1 = data[getIndexOfMemAddress(address1, numInstructions)]
        # Word 1
    if address2 < 96 + (4 * numInstructions): # For Instruction
        data2 = instructions[getIndexOfMemAddress(address2, numInstructions)]
    else: # For Data
        data2 = data[getIndexOfMemAddress(address2, numInstructions)]

    
    # For when we Write to Mem. Select which word to write
    if isWriteToMem and dataWord == 0:
        data1 = dataToWrite
    elif isWriteToMem and dataWord == 1:
        data2 = dataToWrite

    # Getting the set and tag(block), we only care about the first word
    setNum = (address1 & setMask) >> 3
    tag = (address1 & tagMask) >> 5

    # Look at cache container. We check the valid bit and the tag
        # Block 0
    hit = False
    if (cacheSets[setNum][0][0] == 1 and cacheSets[setNum][0][2] == tag):
        # We have a hit
        hit = True
        assocblock = 0 # block zero is the hit
    elif cacheSets[setNum][1][0] == 1 and cacheSets[setNum][1][2] == tag:
        # We have a hit
        hit = True
        assocblock = 1 # block one is the hit
    

    # If hit, update the LRU and if we have a write to memory we update the dirty bit and return
    if hit:
        if hit and isWriteToMem: # hit and writ to data mem instruction
            cacheSets[setNum][assocblock][1] = 1 # update the dirty bit of the block that had the hit
            lruBit[setNum] = (assocblock + 1) % 2 # update lru bit
            cacheSets[setNum][assocblock][dataWord+3] = dataToWrite # updates the word with new data. +3 is used for offset
        elif hit:
            lruBit[setNum] = (assocblock + 1) % 2 # update lru bit
        
        return [True, cacheSets[setNum][assocblock][dataWord + 3]] # return true for hit and the data inside the specific word
    
    # We have a miss if we make it this far
    if address1 in justMissedList: # address was missed in the last cycle
        # remove address from list
        while justMissedList.count(address1) > 0:
            justMissedList.remove(address1)
        
        # need to write back to memory
        if cacheSets[setNum][lruBit[setNum]][1] == 1:
            wbAddr = cacheSets[setNum][lruBit[setNum]][2] # tag 
            # drop the 2 lower bits to get original address
            wbAddr = (wbAddr << 5) + (setNum << 3)

            # write back to main memory for both words
            if wbAddr >= (numInstructions * 4) + 96:
                data[getIndexOfMemAddress(wbAddr, numInstructions)] = cacheSets[setNum][lruBit[setNum]][3]
            
            if wbAddr + 4 >= (numInstructions * 4) + 96:
                data[getIndexOfMemAddress(wbAddr + 4, numInstructions)] = cacheSets[setNum][lruBit[setNum]][4]
            
        # update cache flags
        cacheSets[setNum][lruBit[setNum]][0] = 1 # valid bit
        cacheSets[setNum][lruBit[setNum]][1] = 0 # reset dirty bit

        # if instruction is write to mem we have to set the dirty bit back to 1
        if (isWriteToMem):
            cacheSets[setNum][lruBit[setNum]][1] = 1
        
        # update both words int the block
        cacheSets[setNum][lruBit[setNum]][2] = tag # tag
        cacheSets[setNum][lruBit[setNum]][3] = data1 # word 0
        cacheSets[setNum][lruBit[setNum]][4] = data2 # word 1
        lruBit[setNum] = (lruBit[setNum] + 1) % 2 # sets lru to opposite

        # gives us the word of the instruction we asked for not instruction + 1
        return [True, cacheSets[setNum][(lruBit[setNum] + 1) % 2][dataWord + 3]]
    
    else: # new missed address
        if justMissedList.count(address1) == 0: # add t just missed list so that in the next cycle it can be processed
            justMissedList.append(address1)
        return [False, 0]


# Helper function to check if the instructions is a load or store instruction
def isMemOp(index):
       if opcode[index] == 1986 or opcode[index]== 1984:
           return True


# TODO Add hazzards for load and store instructions
# Issue Unit
class issueUnit:
    global preIssueBuff
    global preAluBuff
    global postAluBuff
    global preMemBuff
    global postMemBuff
    global src1
    global src2
    global dest

    def run(self):

        numIssued = 0 # number of issued instructions
        curr = 0 # current instruction we are analysing for hazards
        numInPreIssueBuff = len(preIssueBuff) - preIssueBuff.count(-1)

        
        while numIssued < 2 and numInPreIssueBuff > 0 and curr < 4:
            index = preIssueBuff[curr]
            issueMe = True

            # Checks for structural hazards
            if isMemOp(index):
                if -1 not in preMemBuff:
                    issueMe = False
            else:
                if -1 not in preAluBuff:
                    issueMe = False
            
            for i in range(0, curr):
                if dest[index] == dest[preIssueBuff[i]]:
                    issueMe = False
                    break # WAW Hazard found in preIssue
            if isMemOp(index):
                for i in range(0, len(preMemBuff)):
                    if preMemBuff[i] != -1:
                        if dest[index] == dest[preMemBuff[i]]:
                            issueMe = False
                            break  # WAW Hazard found in preMem
            if not isMemOp(index):
                for i in range(0, len(preAluBuff)):
                    if preAluBuff[i] != -1:
                        if dest[index] == dest[preAluBuff[i]]:
                            issueMe = False
                            break  # WAW Hazard found in preAlu
            for i in range(0, curr):
                if src1[index] == dest[preIssueBuff[i]] or src2 == dest[preIssueBuff[i]]:
                    issueMe = False
                    break # RAW Hazard found in preIssue
            if isMemOp(index):
                for i in range(0, len(preMemBuff)):
                    if preMemBuff[i] != -1:
                        if src1[index] == dest[preMemBuff[i]] or src2[index] == dest[preMemBuff[i]]:
                            issueMe = False
                            break  # RAW Hazard found in preMem
            if not isMemOp(index):
                for i in range(0, len(preAluBuff)):
                    if preAluBuff[i] != -1:
                        if src1[index] == dest[preAluBuff[i]] or src2[index] == dest[preAluBuff[i]]:
                            issueMe = False
                            break  # RAW Hazard found in preAlu
            if isMemOp(index):
                # for i in range(0,len(postMemBuff)):
                #     if postMemBuff[i] != -1:
                #         if src1[index] == dest[postMemBuff[0]] or src2[index] == dest[postMemBuff[1]]:
                #             issueMe = False
                #             break  # RAW Hazard found in postMem
                if postMemBuff[1] != -1:
                    if src1[index] == dest[postMemBuff[1]] or src2[index] == dest[postMemBuff[1]]:
                        issueMe = False
                        break  # RAW Hazard found in postMem
            if not isMemOp(index):
                # for i in range(0, len(postAluBuff)):
                #     if postAluBuff[i] != -1:
                #         if src1[index] == dest[preAluBuff[0]] or src2[index] == dest[preAluBuff[1]]:
                #             issueMe = False
                #             break  # RAW Hazard found in postAlu
                if postAluBuff[1] != -1:
                        if src1[index] == dest[postAluBuff[1]] or src2[index] == dest[postAluBuff[1]]:
                            issueMe = False
                            break  # RAW Hazard found in postAlu
            
            # TODO Deal with store instruction being before load instructions

            if issueMe:
                numIssued += 1
                # copy the instruction from preIssue to either preMem or preAlu
                if isMemOp(index):
                    preMemBuff[preMemBuff.index(-1)] = index
                else:
                    preAluBuff[preAluBuff.index(-1)] = index


                # preIssueBuff[0:curr] = preIssueBuff[0:curr]
                # print"pre " + str(preIssueBuff[curr+1])
                preIssueBuff[curr:3] = preIssueBuff[curr+1:] # shifts elements left overwriting curr
                preIssueBuff[3] = -1 # sets the last element to empty 
                numInPreIssueBuff -= 1 
            else:
                curr += 1 # skips current instruction and checks the next instruction


# Write Back Unit
class writeBack:

    global postAluBuff
    global postMemBuff
    global reg
    global dest 

    def run(self):
        if postAluBuff[1] != -1:
            reg[dest[postAluBuff[1]]] = postAluBuff[0]
            postAluBuff[0] = -1
            postAluBuff[1] = -1
        if postMemBuff[1] != -1:
            reg[dest[postAluBuff[1]]] = postMemBuff[0]
            postMemBuff[0] = -1
            postMemBuff[1] = -1


# ALU Unit
class ALU:
    
    

    def run(self):
        global preAluBuff
        global postAluBuff
        global arg1
        global arg2

        # opcode of instruction we are looking at
        instruction = 0

        # Checks to see whats in preBuff and updates it
        if preAluBuff[0] != -1:
            instruction = opcode[preAluBuff[0]]
            index = preAluBuff[0]
            if preAluBuff[1] != -1:
                preAluBuff[0] = preAluBuff[1]
                preAluBuff[1] = -1
            else:
                preAluBuff[0] = -1
            
            postAluBuff[1] = index
        
         # ADD
        if instruction == 1112:
            postAluBuff[0] = reg[int(arg1[index])] + reg[int(arg2[index])]

        # SUB
        if instruction == 1624:
            postAluBuff[0] = reg[int(arg1[index])] - reg[int(arg2[index])]

        # AND
        if instruction == 1104:
            postAluBuff[0] = reg[int(arg1[index])] & reg[int(arg2[index])]

        # OR
        if instruction == 1360:
            postAluBuff[0] = reg[int(arg1[index])] | reg[int(arg2[index])]

        # ADDI
        if 1160 <= instruction <= 1161:
            postAluBuff[0] = reg[int(arg1[index])] + int(arg2[index])

        # EOR
        if instruction == 1872:
            postAluBuff[0] = reg[int(arg1[index])] ^ reg[int(arg2[index])]

        # SUBI
        if 1672 <= instruction <= 1673:
            postAluBuff[0] = reg[int(arg1[index])] - int(arg2[index])

        # LSL
        if instruction == 1691:
            postAluBuff[0] = reg[int(arg2[index])] << int(arg1[index])

        # LSR
        if instruction == 1690:
            postAluBuff[0] = (reg[int(arg2[index])] % (1 << 64)) >> int(arg1[index])

        # ASR
        if instruction == 1692:
            postAluBuff[0] = reg[int(arg1[index])] >> int(arg2[index])

        # MOVZ
        if 1684 <= instruction <= 1687:
            postAluBuff[0] = int(arg2[index]) << (int(arg1[index] * 16))

        # MOVK
        if 1940 <= instruction <= 1943:
            if arg1[index] == 0:
                postAluBuff[0] = (reg[arg3[index]] % (1 << 64)) >> 16
                postAluBuff[0] = reg[arg3[index]] << 16
                postAluBuff[0] = int(reg[arg3[index]] ^ arg2[index])


            elif arg1[index] == 1:
                rightSplitMask = 0x000000FF
                rightSplit = rightSplitMask & reg[arg3[index]]
                leftSplit = (reg[arg3[index]] % (1 << 64)) >> 32
                leftShiftedSplit = leftSplit << 32
                immShifted = arg2[index] << 16

                postAluBuff[0] = rightSplit ^ immShifted
                postAluBuff[0] = int(reg[arg3[index]] ^ leftShiftedSplit)

            elif arg1[index] == 2:
                rightSplitMask = 0x0000FFFF
                rightSplit = rightSplitMask & reg[arg3[index]]
                leftSplit = (reg[arg3[index]] % (1 << 64)) >> 48
                leftShiftedSplit = leftSplit << 48
                immShifted = arg2[index] << 32

                postAluBuff[0] = rightSplit ^ immShifted
                postAluBuff[0] = int(reg[arg3[index]] ^ leftShiftedSplit)

            elif arg1[index] == 3:
                rightSplitMask = 0x00FFFFFF
                rightSplit = rightSplitMask & reg[arg3[index]]
                immShifted = arg2[index] << 48

                postAluBuff[0] = int(rightSplit ^ immShifted)
        

# Fetch Unit
class fetchUnit:
    

    def run(self):
        global fetchPC
        global dataSwitch
        global preIssueBuff
        global opcode
        global mempc
        global clearCounter

        # TODO: Will have to refactor for data

        # instruction I'm currently looking at
        if fetchPC in mempc:
            instructionIndex = mempc.index(fetchPC)

        # Fetching instructions/Data
        if dataSwitch:

            # access cache TODO: May have to check for outlier case after BREAK PC may go out of bound
            # for now we won't use [1] the data it returns
            # TODO: Figure out how to deal with data
            cacheFetch = accessMem(-1, instructionIndex, 0, 0)
        

            # if cache misses we stall and return to simulator
            if cacheFetch[0] == False:
                return True

            # Check to see if we have space in preIssueBuffer
            if -1 in preIssueBuff:

                # Check for branch instructionsf
                if 160 <= opcode[instructionIndex] <= 191:
                    return True
                    # TODO: figure this shit out. Don't have to check for hazard
                if 1440 <= opcode[instructionIndex] <= 1447 or 1448 <= opcode[instructionIndex] <= 1455:
                    return True
                    # TODO: figure this shit out as well. Have to check for hazard

                # Check for break
                # if opcode[instructionIndex] == 2038 or opcode[instructionIndex + 1] == 2038:
                #     # update PC and switch to data
                #     fetchPC += 8
                #     dataSwitch = False
                #     return True
                # else:
                # Two or more spaces available in preIssueBuffer
                if preIssueBuff.count(-1) > 1:
                    # Check for NOP
                    if opcode[instructionIndex] == 0:
                        
                        if opcode[instructionIndex + 1] == 0: # Both instructions are NOP
                            fetchPC += 8
                            return True

                        # Only the firt one is NOP
                        # Check for break
                        if opcode[instructionIndex + 1] == 2038:
                            fetchPC += 8
                            dataSwitch = False
                            return True
                        else:
                            preIssueBuff[preIssueBuff.index(-1)] = instructionIndex + 1
                            fetchPC += 8
                            return True

                    elif opcode[instructionIndex + 1] == 0:
                        # Scond one is NOP
                        preIssueBuff[preIssueBuff.index(-1)] = instructionIndex
                        fetchPC += 8
                        return True
                    else:
                        # No NOP
                        if opcode[instructionIndex + 1] == 2038:
                            preIssueBuff[preIssueBuff.index(-1)] = instructionIndex
                            fetchPC += 8
                            dataSwitch = False
                            return True
                        else: 
                            preIssueBuff[preIssueBuff.index(-1)] = instructionIndex
                            preIssueBuff[preIssueBuff.index(-1)] = instructionIndex + 1
                            fetchPC += 8
                            return True
                else:
                    # Check for NOP
                    if opcode[instructionIndex] == 0:
                        
                        if opcode[instructionIndex + 1] == 0: # Both instructions are NOP
                            fetchPC += 8
                            return True

                        # Only the firt one is NOP
                        if opcode[instructionIndex + 1] == 2038:
                            fetchPC += 8
                            dataSwitch = False
                            return True
                        else:
                            preIssueBuff[preIssueBuff.index(-1)] = instructionIndex + 1
                            fetchPC += 8
                            return True

                    elif opcode[instructionIndex + 1] == 0:
                        # Scond one is NOP
                        preIssueBuff[preIssueBuff.index(-1)] = instructionIndex
                        fetchPC += 8
                        return True
                    else:
                        # None are NOP, fetch the first instruction
                        if opcode[instructionIndex + 1] == 2038:
                            preIssueBuff[preIssueBuff.index(-1)] = instructionIndex
                            fetchPC += 8
                            dataSwitch = False
                            return True
                        else:
                            preIssueBuff[preIssueBuff.index(-1)] = instructionIndex
                            fetchPC += 4
                            return True
            else:
                return True
        else:
            # TODO: Do data stuff

            instructionsProcessed = True
            

            for i in range(len(preIssueBuff)):
                if preIssueBuff[i] != -1:
                    instructionsProcessed = False

            for i in range(len(preAluBuff)):
                if preAluBuff[i] != -1:
                    instructionsProcessed = False
                if preMemBuff[i] != -1:
                    instructionsProcessed = False
            
            if instructionsProcessed:
                clearCounter += 1
                # All instruction are finished and we have a clear output
                if clearCounter == 2:
                    return False
            else:
                return True
        
        return True
        

class Simmulator:

    # Units to process instructions
    

    def run(self):
        global arg1

        iu = issueUnit()
        wb = writeBack()
        alu = ALU()
        fu = fetchUnit()
        cycle = 1
        go = True

        while go:
            wb.run()
            alu.run()
            iu.run()
            go = fu.run()
            self.printState(cycle)
            cycle += 1

    
    def printState(self, cycle):

        global preIssueBuff
        global preAluBuff
        global preMemBuff
        global postAluBuff 
        global postMemBuff
        global cacheSets
        global reg

        
        print("Cycle: " + str(cycle) + "\n")
        print("Pre-Issue Buffer: " + str(preIssueBuff) + "\n")
        print("Pre_ALU Queue: " + str(preAluBuff) + "\n")
        print("Post_ALU Queue: " + str(postAluBuff) + "\n")
        print("Pre_MEM Queue: " + str(preMemBuff) + "\n")
        print("Post_MEM Queue: " + str(postMemBuff) + "\n")
        print("Reg: " + str(reg) + "\n")
        print("Cache: " + str(cacheSets) + "\n")
        



sim = Simmulator()
sim.run()