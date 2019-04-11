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
        global mem
        global binMem
        global opcode
        global mempc
        global instructionString
        global inputFileName
        global outputFileName

        pc = 0

        for i in range(len(sys.argv)):
            if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
                inputFileName = sys.argv[i + 1]
                print(inputFileName)
            elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
                outputFileName = sys.argv[i + 1]



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

        # Starts a local mempc
        local_mempc = mempc[0]
        cycle = 1

        # Initializes all 32 registers to 0
        reg = [0]*32


        startDataAddressIndex = (len(mempc) - len(data)) - 1

        print (startDataAddressIndex)
        print (mempc)

        if len(data) != 0:
            startDataAddress = mempc[startDataAddressIndex]
        else:
            startDataAddress = mempc[startDataAddressIndex] + 4


        is_looping = True

        while True:

            for i in range(len(mempc)):
                if local_mempc == mempc[i]:
                    instruction = opcode[i]
                    index = i



            # ADD
            if instruction == 1112:
                reg[arg3[index]] = reg[arg1[index]] + reg[arg2[index]]
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # SUB
            if instruction == 1624:
                reg[arg3[index]] = reg[arg1[index]] - reg[arg2[index]]
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # AND
            if instruction == 1104:
                reg[arg3[index]] = reg[arg1[index]] & reg[arg2[index]]
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # OR
            if instruction == 1360:
                reg[arg3[index]] = reg[arg1[index]] | reg[arg2[index]]
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # ADDI
            if 1160 <= instruction <= 1161:
                reg[arg3[index]] = reg[arg1[index]] + arg2[index]
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # EOR
            if instruction == 1872:
                reg[arg3[index]] = reg[arg1[index]] ^ reg[arg2[index]]
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # SUBI
            if 1672 <= instruction <= 1673:
                reg[arg3[index]] = reg[arg1[index]] - arg2[index]
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # LSL
            if instruction == 1691:
                reg[arg3[index]] = reg[arg2[index]] << arg1[index]
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # LSR
            if instruction == 1690:
                reg[arg3[index]] = (reg[arg2[index]] % (1 << 64)) >> arg1[index]
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # ASR
            if instruction == 1692:
                reg[arg3[index]] = reg[arg1[index]] >> arg2[index]
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # B
            if 160 <= instruction <= 191:
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += arg1[index] * 4
            # CBZ
            if 1440 <= instruction <= 1447:
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                if reg[arg2[index]] == 0:
                    local_mempc += arg1[index] * 4
                else:
                    local_mempc += 4
            # CBNZ
            if 1448 <= instruction <= 1455:
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                if reg[arg2[index]] != 0:
                    local_mempc += arg1[index] * 4
                else:
                    local_mempc += 4
            #MOVZ
            if 1684 <= instruction <= 1687:
                reg[arg3[index]] = arg2[index] << (arg1[index] * 16)
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            #MOVK
            if 1940 <= instruction <= 1943:
                if arg1[index] == 0:
                    reg[arg3[index]] = (reg[arg3[index]] % (1 << 64)) >> 16
                    reg[arg3[index]] = reg[arg3[index]] << 16
                    reg[arg3[index]] = reg[arg3[index]] ^ arg2[index]


                elif arg1[index] == 1:
                    rightSplitMask = 0x000000FF
                    rightSplit = rightSplitMask & reg[arg3[index]]
                    leftSplit = (reg[arg3[index]] % (1 << 64)) >> 32
                    leftShiftedSplit = leftSplit << 32
                    immShifted = arg2[index] << 16

                    reg[arg3[index]] = rightSplit ^ immShifted
                    reg[arg3[index]] =reg[arg3[index]] ^ leftShiftedSplit

                elif arg1[index] == 2:
                    rightSplitMask = 0x0000FFFF
                    rightSplit = rightSplitMask & reg[arg3[index]]
                    leftSplit = (reg[arg3[index]] % (1 << 64)) >> 48
                    leftShiftedSplit = leftSplit << 48
                    immShifted = arg2[index] << 32

                    reg[arg3[index]] = rightSplit ^ immShifted
                    reg[arg3[index]] = reg[arg3[index]] ^ leftShiftedSplit

                elif arg1[index] == 3:
                    rightSplitMask = 0x00FFFFFF
                    rightSplit = rightSplitMask & reg[arg3[index]]
                    immShifted = arg2[index] << 48

                    reg[arg3[index]] = rightSplit ^ immShifted

                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # STUR
            if instruction == 1984:
                address = (arg3[index] * 4) + reg[arg2[index]]
                data[getMemIndex(address, startDataAddress)] = reg[arg1[index]]
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # LDUR
            if instruction == 1986:
                address = (arg3[index] * 4) + reg[arg2[index]]
                reg[arg1[index]] = data[getMemIndex(address, startDataAddress)]
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # NOP
            if instruction == 0:
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                local_mempc += 4
            # BREAK
            elif instruction == 2038:
                is_looping = False
                printCycle(cycle, mempc[index], instructionString[index], startDataAddress)
                print("Break")

            cycle += 1

            if not is_looping:
                break


def printCycle(cycle, mempc, instruction_string, startDataAddress):

    if cycle == 1:
        f = open(outputFileName + "_sim.txt", 'w')
    else:
        f = open(outputFileName + "_sim.txt", 'a')

    print ("File open")
    f.write("=" * 20 + '\n')
    f.write("cycle:"+ str(cycle) + '\t' + str(mempc) + '\t' + instruction_string + '\n\n')
    f.write("registers:" + '\n')
    f.write("r00:" + "\t" + str(reg[0]) + "\t" + str(reg[1]) + "\t" + str(reg[2]) + "\t" + str(reg[3]) + "\t"
            + str(reg[4]) + "\t" + str(reg[5]) + "\t" + str(reg[6]) + "\t" + str(reg[7]) + "\n")
    f.write("r08:" + "\t" + str(reg[8]) + "\t" + str(reg[9]) + "\t" + str(reg[10]) + "\t" + str(reg[11]) + "\t"
            + str(reg[12]) + "\t" + str(reg[13]) + "\t" + str(reg[14]) + "\t" + str(reg[15]) + "\n")
    f.write("r16:" + "\t" + str(reg[16]) + "\t" + str(reg[17]) + "\t" + str(reg[18]) + "\t" + str(reg[19]) + "\t"
            + str(reg[20]) + "\t" + str(reg[21]) + "\t" + str(reg[22]) + "\t" + str(reg[23]) + "\n")
    f.write("r24:" + "\t" + str(reg[24]) + "\t" + str(reg[25]) + "\t" + str(reg[26]) + "\t" + str(reg[27]) + "\t"
            + str(reg[28]) + "\t" + str(reg[29]) + "\t" + str(reg[30]) + "\t" + str(reg[31]) + "\n\n")
    f.write("data:")


    for i in range(len(data)):

        if i % 8 != 0:
            f.write(str(data[i]) + "\t")
        else:
            f.write("\n" + str(startDataAddress) + ":\t" + str(data[i]) + "\t")
            startDataAddress += 4 * 8

    f.write("\n")

    f.close()


def getMemIndex(address, startAddress):


    index = (address - startAddress) / 4

    if index > len(data):
        fullIndex = (index % 7) + index + 1
        for i in range(fullIndex - len(data)):
            data.append(0)


    return index












sim = Simulator()
sim.run()





