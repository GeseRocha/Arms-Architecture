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

#file names
outputFileName = ''
inputFileName = ''

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
        #global mem
        #global binMem
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
        inputFileName = 'R_type_test.txt'
        outputFileName = 'R_type_test_output'



        instructions = [line.rstrip() for line in open(inputFileName, 'rb')]

        # Translating instructions
        for i in range(len(instructions)):
            opcode.append(int(instructions[i][0:11], 2))

            # This section is for R format instructions
            if opcode[i] == 1112:

                opcodeStr.append("ADD")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
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

        print(outputFileName)


dissme = Dissasembler()
dissme.run()





def accessMem(testNum):
    return testNum + 1


