import sys
import matplotlib.pyplot as plt


time = [1]
x_cord = []
y_cord = []

class data:
    Halted  = False
    PC = 0
    Reg_val  = {"000":0, "001":0, "010":0, "011":0, "100":0, "101":0, "110":0, "111":0}
    Memory = {}

def d2b(num):

    s = bin(num).replace("0b", "")
    s = str(s)
    l = len(s)
    if len(s) < 16:
        while len(s) < 16:
            s = "0" + s

    return s

def b2d(string):

    binary = int(string)
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return(decimal)

def ADD(r1, r2, r3, Data):
    val = Data.Reg_val[r2] + Data.Reg_val[r3]
    if val >= 2**16:
        Data.Reg_val["111"] = 8
    else:
        Data.Reg_val["111"] = 0
        Data.Reg_val[r1] = val
    Data.PC  = Data.PC + 1

## this ##
def SUB(r1, r2, r3, Data):
    val = Data.Reg_val[r2] - Data.Reg_val[r3]
    if val < 0:
        Data.Reg_val["111"] = 8
    else:
        Data.Reg_val["111"] = 0
        Data.Reg_val[r1] = val
    Data.PC += 1

def Move_I(r1,imm,Data):
    temp = b2d(imm)
    Data.Reg_val[r1] = temp
    Data.Reg_val["111"]  = 0
    Data.PC += 1

def Move_R(r1,r2,Data):
    Data.Reg_val[r1] = Data.Reg_val[r2]
    Data.Reg_val["111"] = 0
    Data.PC += 1

def Load(r1,mem_add,Data):
    Data.Reg_val[r1] = b2d(Data.Memory[mem_add])
    Data.Reg_val["111"] = 0
    Data.PC += 1
    x_cord.append(time[0])
    y_cord.append(mem_add)

def Store(r1,mem_add,Data):
    Data.Memory[mem_add] = d2b(Data.Reg_val[r1])
    Data.Reg_val["111"] = 0
    Data.PC += 1
    x_cord.append(time[0])
    y_cord.append(mem_add)

def Mul(r1,r2,r3,Data):
    val = (Data.Reg_val[r2]) * (Data.Reg_val[r3])

    if val >= 2**16:
        Data.Reg_val["111"] = 8
    else:
        Data.Reg_val["111"] = 0
        Data.Reg_val[r1] = val
    Data.PC += 1

def Div(r1,r2,Data):
    qu = (Data.Reg_val[r1]) // (Data.Reg_val[r2])
    rem = (Data.Reg_val[r1]) % (Data.Reg_val[r2])
    Data.Reg_val["000"] = qu
    Data.Reg_val["001"] = rem
    Data.Reg_val["111"] = 0
    Data.PC += 1

def RightS(r1,imm,Data):
    temp = b2d(imm)
    Data.Reg_val[r1] = (Data.Reg_val[r1]) // (2**temp)
    Data.Reg_val["111"] = 0
    Data.PC += 1

def LeftS(r1,imm,Data):
    temp = b2d(imm)
    val = Data.Reg_val[r1] * (2**temp)
    if val >= 2**16:
        Data.Reg_val["111"] = 8
    else:
        Data.Reg_val["111"] = 0
    Data.Reg_val[r1] = val

    Data.PC += 1

def XOR (r1,r2,r3,Data):

    r2_binary = d2b(Data.Reg_val[r2])
    r3_binary = d2b(Data.Reg_val[r3])
    st = ""

    for i in range (0,16):

        if r2_binary[15 - i] == r3_binary[15 - i]:
            st = "0" + st

        else:
            st = "1" + st

    Data.Reg_val[r1] = b2d(st)
    Data.Reg_val["111"] = 0
    Data.PC += 1

def OR(r1,r2,r3,Data):

    r2_binary = d2b(Data.Reg_val[r2])
    r3_binary = d2b(Data.Reg_val[r3])
    st = ""

    for i in range (0,16):

        if int(r2_binary[15 - i]) + int(r3_binary[15 - i]) > 0:
            st = "1" + st

        else:
            st = "0" + st

    Data.Reg_val[r1] = b2d(st)
    Data.Reg_val["111"] = 0
    Data.PC += 1

def AND(r1,r2,r3,Data):

    r2_binary = d2b(Data.Reg_val[r2])
    r3_binary = d2b(Data.Reg_val[r3])
    st = ""

    for i in range (0,16):

        if int(r2_binary[15 - i]) +int(r3_binary[15 - i]) == 2:
            st = "1" + st

        else:
            st = "0" + st

    Data.Reg_val[r1] = b2d(st)
    Data.Reg_val["111"] = 0
    Data.PC += 1

def Invert(r1,r2,Data):

    r2_binary = d2b(Data.Reg_val[r2])
    st = ""

    for i in range (0,16):

        if int(r2_binary[15 - i]) == "0":
            st = "1" + st

        else:
            st = "0" + st

    Data.Reg_val[r1] = b2d(st)
    Data.Reg_val["111"] = 0
    Data.PC += 1

def Compare(r1,r2,Data):
    if Data.Reg_val[r1] > Data.Reg_val[r2]:
        Data.Reg_val["111"] = 2

    elif Data.Reg_val[r1] < Data.Reg_val[r2]:
        Data.Reg_val["111"] = 4

    else:
        Data.Reg_val["111"] = 1

    Data.PC += 1

def U_Jump(mem_addr,Data):
    Data.PC = b2d(mem_addr)
    Data.Reg_val["111"] = 0

def L_Jump(mem_addr,Data):
    if Data.Reg_val["111"] == 4:
        Data.PC = b2d(mem_addr)
    else:
        Data.PC += 1
    Data.Reg_val["111"] = 0

def G_Jump(mem_addr,Data):
    if Data.Reg_val["111"] == 2:
        Data.PC = b2d(mem_addr)
    else:
        Data.PC += 1
    Data.Reg_val["111"] = 0

def E_Jump(mem_addr,Data):
    if Data.Reg_val["111"] == 1:
        Data.PC = b2d(mem_addr)
    else:
        Data.PC += 1
    Data.Reg_val["111"] = 0

def Halt(Data):
    Data.Halted = True
    Data.Reg_val["111"] = 0
    Data.PC += 1

def driver(instruction, Data):
    opcode = instruction[0:5]
    if opcode == "10000":
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:16]
        ADD(r1, r2, r3, Data)

    elif opcode == "10001":
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:16]
        SUB(r1,r2,r3,Data)

    elif opcode == "10010":
        r1 = instruction[5:8]
        imm = instruction[8:16]
        Move_I(r1,imm,Data)

    elif opcode == "10011":
        r1 = instruction[10:13]
        r2 = instruction[13:16]
        Move_R(r1,r2,Data)

    elif opcode == "10100":
        r1 = instruction[5:8]
        mem_add = b2d(instruction[8:16])
        Load(r1,mem_add,Data)

    elif opcode == "10101":
        r1 = instruction[5:8]
        mem_add = b2d(instruction[8:16])
        Store(r1,mem_add,Data)

    elif opcode == "10110":
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:16]
        Mul(r1,r2,r3,Data)

    elif opcode == "10111":
        r1 = instruction[10:13]
        r2 = instruction[13:16]
        Div(r1,r2,Data)

    elif opcode == "11000":
        r1 = instruction[5:8]
        imm = instruction[8:16]
        RightS(r1, imm,Data)

    elif opcode == "11001":
        r1 = instruction[5:8]
        imm = instruction[8:16]
        LeftS(r1,imm,Data)

    elif opcode == "11010":
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:16]
        XOR(r1,r2,r3,Data)

    elif opcode == "11011":
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:16]
        OR(r1,r2,r3,Data)

    elif opcode == "11100":
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:16]
        AND(r1,r2,r3,Data)

    elif opcode == "11101":
        r1 = instruction[10:13]
        r2 = instruction[13:16]
        Invert(r1,r2,Data)

    elif opcode == "11110":
        r1 = instruction[10:13]
        r2 = instruction[13:16]
        Compare(r1,r2,Data)

    elif opcode == "11111":
        mem_addr = instruction[8:16]
        U_Jump(mem_addr, Data)

    elif opcode == "01100":
        mem_addr = instruction[8:16]
        L_Jump(mem_addr, Data)

    elif opcode == "01101":
        mem_addr = instruction[8:16]
        G_Jump(mem_addr,Data)

    elif opcode == "01111":
        mem_addr = instruction[8:16]
        E_Jump(mem_addr,Data)

    elif opcode == "01010":
        Halt(Data)

def main(Data):

    for i in range(0, 256):  # initialize the memory
        Data.Memory[i] = "0000000000000000"

    inst = 0  # read the input binary file and update the memory
    for line in sys.stdin:
        Data.Memory[inst] = line
        inst = inst + 1

    while not Data.Halted:
        x_cord.append(time[0])
        y_cord.append(Data.PC)

        instruction = Data.Memory[Data.PC]
        Temp_pc  = Data.PC

        driver(instruction,Data)

        time[0] += 1

        print((d2b(Temp_pc))[8:16], d2b(Data.Reg_val["000"]), d2b(Data.Reg_val["001"]), d2b(Data.Reg_val["010"]),
              d2b(Data.Reg_val["011"]), d2b(Data.Reg_val["100"]), d2b(Data.Reg_val["101"]), d2b(Data.Reg_val["110"]),
              d2b(Data.Reg_val["111"]))


    for i in Data.Memory:
        print(Data.Memory[i])



Data = data()
main(Data)

plt.scatter(x_cord, y_cord)
plt.title = ('Memory Access Trace')
plt.xlabel('Cycle Number')
plt.ylabel('Memory Address Accessed')
plt.show()