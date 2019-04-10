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
        global mem
        global binMem
        global opcode
        global mempc
        global instructionString

        pc = 0

        for i in range(len(sys.argv)):
            if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
                inputFileName = sys.argv[i + 1]
                print(inputFileName)
            elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
                outputFileName = sys.argv[i + 1] + "_dis.txt"



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
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
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
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
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
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
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
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
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
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
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
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
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
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
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
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
                instrSpaced.append(bin2StrSpacedRandD(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif opcode[i] == 0:
                arg1.append(0)
                arg2.append(0)
                arg3.append(0)
                arg1Str.append("")
                arg2Str.append("")
                arg3Str.append("")
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
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
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
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
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
                instrSpaced.append(bin2StrSpacedRandD(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif 160 <= opcode[i] <= 191:
                opcodeStr.append("B")
                arg1.append(int(instructions[i], base=2) & addr3Mask)
                arg2.append(0)
                arg3.append(0)
                arg1Str.append("\t#" + str(imm32Bit2ComplementToDec(immBitTo32BitConverter(arg1[i], 26))))
                arg2Str.append('')
                arg3Str.append('')
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
                instrSpaced.append(bin2StringSpacedB(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif 1440 <= opcode[i] <= 1447:
                opcodeStr.append("CBZ")
                arg1.append((int(instructions[i], base=2) & addr2Mask) >> 5)
                arg2.append((int(instructions[i], base=2) & rdMask) >> 0)
                arg3.append(0)
                arg1Str.append("\tR" + str(arg2[i]))
                arg2Str.append(", #" + str(imm32Bit2ComplementToDec(immBitTo32BitConverter(arg1[i], 19))))
                arg3Str.append("")
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
                instrSpaced.append(bin2StringSpacedCB(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif 1448 <= opcode[i] <= 1455:
                opcodeStr.append("CBNZ")
                arg3.append(0)
                arg1.append((int(instructions[i], base=2) & addr2Mask) >> 5)
                arg2.append((int(instructions[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg2[i]))
                arg2Str.append(", #" + str(imm32Bit2ComplementToDec(immBitTo32BitConverter(arg1[i], 19))))
                arg3Str.append("")
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
                instrSpaced.append(bin2StringSpacedCB(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif 1684 <= opcode[i] <= 1687:

                opcodeStr.append("MOVZ")
                arg1.append((int(instructions[i], base=2) & imsftMask) >> 21)
                arg2.append((int(instructions[i], base=2) & imdataMask) >> 5)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", " + str(arg2[i]))
                arg3Str.append(", LSL " + str(arg1[i]))
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
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
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
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
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
                instrSpaced.append(bin2StrSpacedRandR(instructions[i]))
                mempc.append(96 + (pc * 4))

            elif opcode[i] == 1692:
                opcodeStr.append("ASR")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                arg1Str.append("\tR" + str(arg3[i]))
                arg2Str.append(", R" + str(arg1[i]))
                arg3Str.append(", R" + str(arg2[i]))
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
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
                instructionString = opcodeStr[i] + arg1Str[i] + arg2Str[i] + arg3Str[i]
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

        with open(outputFileName, 'w') as f:
            for i in range(len(mempc) - len(data)):
                f.write((instrSpaced)[i])
                f.write("\t"+str(mempc[i])+"\t")
                f.write((opcodeStr)[i])
                f.write((arg1Str)[i])
                f.write((arg2Str)[i])
                f.write((arg3Str)[i])
                f.write("\n")

            for i in range(len(data)):
                f.write(bindata[i])
                f.write("\t" + str(mempc[(len(mempc) - len(data)) + i]))
                f.write("\t" + str(data[i]))
                f.write("\n")

        print(outputFileName)


dissme = Dissasembler()
dissme.run()


class Simulator():

    def run(self):
        global opcodeStr
        global instrSpaced
        global arg1
        global arg2
        global arg3
        global arg1Str
        global arg2Str
        global arg3Str
        global mem
        global binMem
        global opcode
        global mempc
        global reg

        local_mempc = mempc[0]
        cycle = 1

        reg = [0]*32
        print (reg)

        is_looping =True

        while True:

            for i in range(len(mempc) - len(data)):

                if opcode[i] == 1112:
                    reg[arg3[i]] = reg[arg1[i]] + reg[arg3[i]]
                    printCycle(cycle, mempc[i], instructionString[i])
                elif opcode[i] == 2038:
                    is_looping = False
                    print("Break")

            if not is_looping:
                break



def printCycle(cycle, mempc, instruction_string):

    print "=" * 20 + '\n'
    print str(cycle) + '\t' + str(mempc) + '\t' + instruction_string + '\n\n'
    print "registers:" + '\n'
    print "r00:" + "\t" + reg[0] + "\t" + reg[1] + "\t" + reg[2] + "\t" + reg[3] + "\t" + reg[4] + "\t" + reg[5] + "\t" \
          + reg[6] + "\t" + reg[7] + "\n"
    print "r08:" + "\t" + reg[8] + "\t" + reg[9] + "\t" + reg[10] + "\t" + reg[11] + "\t" + reg[12] + "\t" + reg[13] + "\t" \
          + reg[14] + "\t" + reg[15] + "\n"
    print "r16:" + "\t" + reg[16] + "\t" + reg[17] + "\t" + reg[18] + "\t" + reg[19] + "\t" + reg[20] + "\t" + reg[21] + "\t" \
          + reg[22] + "\t" + reg[23] + "\n"
    print "r24:" + "\t" + reg[24] + "\t" + reg[25] + "\t" + reg[26] + "\t" + reg[27] + "\t" + reg[28] + "\t" + reg[29] + "\t" \
          + reg[30] + "\t" + reg[31] + "\n\n"
    print "data:"



sim = Simulator()
sim.run()





