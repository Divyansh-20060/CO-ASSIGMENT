import sys

def d2b(num):

    s = bin(num).replace("0b", "")
    s = str(s)
    l = len(s)
    if len(s) < 16:
        while len(s) < 8:
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

def ADD(r1, r2, r3, reg_val, pc):
    val = reg_val[r2] + reg_val[r3]
    if val >= 2**16:
        reg_val["111"] = 8
    else:
        reg_val["111"] = 0
        reg_val[r1] = val
    pc += 1

## this ##
def SUB(r1, r2, r3, reg_val, pc):
    val = reg_val[r2] - reg_val[r3]
    if val < 0:
        x = 0
        reg_val["111"] = 8
    else:
        reg_val["111"] = 0
        reg_val[r1] = val
    pc += 1

def Move_I(r1,imm,reg_val,pc):
    temp = b2d(imm)
    reg_val[r1] = temp
    reg_val["111"]  = 0
    pc += 1

def Move_R(r1,r2,reg_val,pc):
    reg_val[r1] = reg_val[r2]
    reg_val["111"] = 0
    pc += 1

def Load(r1,mem_add,memory,reg_val,pc):
    reg_val[r1] = b2d(memory[mem_add])
    reg_val["111"] = 0
    pc += 1

def Store(r1,mem_add,memory,reg_val,pc):
    memory[mem_add] = d2b(reg_val[r1])
    reg_val["111"] = 0
    pc += 1

def Mul(r1,r2,r3,reg_val,pc):
    val = (reg_val[r2]) * (reg_val[r3])

    if val >= 2**16:
        reg_val["111"] = 8
    else:
        reg_val["111"] = 0
        reg_val[r1] = val
    pc += 1

def Div(r1,r2,reg_val,pc):
    qu = (reg_val[r1]) // (reg_val[r2])
    rem = (reg_val[r1]) % (reg_val[r2])
    reg_val["000"] = qu
    reg_val["001"] = rem
    reg_val["111"] = 0
    pc += 1

def RightS(r1,imm,reg_val,pc):
    temp = b2d(imm)
    reg_val[r1] = (reg_val[r1]) // (2**temp)
    reg_val["111"] = 0
    pc += 1

def LeftS(r1,imm,reg_val,pc):
    temp = b2d(imm)
    val = reg_val[r1] * (2**temp)
    if val >= 2**16:
        reg_val["111"] = 8
    else:
        reg_val["111"] = 0
    reg_val[r1] = val

    pc += 1

def XOR (r1,r2,r3,reg_val,pc):

    r2_binary = d2b(reg_val[r2])
    r3_binary = d2b(reg_val[r3])
    st = ""

    for i in range (0,16):

        if r2_binary[15 - i] == r3_binary[15 - i]:
            st = "0" + st

        else:
            st = "1" + st

    reg_val[r1] = b2d(st)
    reg_val["111"] = 0
    pc += 1

def OR(r1,r2,r3,reg_val,pc):

    r2_binary = d2b(reg_val[r2])
    r3_binary = d2b(reg_val[r3])
    st = ""

    for i in range (0,16):

        if int(r2_binary[15 - i]) + int(r3_binary[15 - i]) > 0:
            st = "1" + st

        else:
            st = "0" + st

    reg_val[r1] = b2d(st)
    reg_val["111"] = 0
    pc += 1

def AND(r1,r2,r3,reg_val,pc):

    r2_binary = d2b(reg_val[r2])
    r3_binary = d2b(reg_val[r3])
    st = ""

    for i in range (0,16):

        if int(r2_binary[15 - i]) +int(r3_binary[15 - i]) == 2:
            st = "1" + st

        else:
            st = "0" + st

    reg_val[r1] = b2d(st)
    reg_val["111"] = 0
    pc += 1

def Invert(r1,r2,reg_val,pc):

    r2_binary = d2b(reg_val[r2])
    st = ""

    for i in range (0,16):

        if int(r2_binary[15 - i]) == "0":
            st = "1" + st

        else:
            st = "0" + st

    reg_val[r1] = b2d(st)
    reg_val["111"] = 0
    pc += 1

def Compare(r1,r2,reg_val,pc):
    if reg_val[r1] > reg_val[r2]:
        reg_val["111"] = 2

    elif reg_val[r1] < reg_val[r2]:
        reg_val["111"] = 4

    else:
        reg_val["111"] = 1

    pc += 1

def U_Jump(mem_addr,pc,reg_val):
    pc = b2d(mem_addr)
    reg_val["111"] = 0

def L_Jump(mem_addr,pc,reg_val):
    if reg_val["111"] == 4:
        pc = b2d(mem_addr)
    else:
        pc += 1
    reg_val["111"] = 0

def G_Jump(mem_addr,pc,reg_val):
    if reg_val["111"] == 2:
        pc = b2d(mem_addr)
    else:
        pc += 1
    reg_val["111"] = 0

def E_Jump(mem_addr,pc,reg_val):
    if reg_val["111"] == 1:
        pc = b2d(mem_addr)
    else:
        pc += 1
    reg_val["111"] = 0

def Halt(halted,reg_val,pc):
    halted = True
    reg_val["111"] = 0
    pc += 1

def driver(instruction, Reg_val, pc,Memory,halted):
    opcode = instruction[0:5]
    if opcode == "10000":
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:16]
        ADD(r1, r2, r3, Reg_val, pc)

    elif opcode == "10001":
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:16]
        SUB(r1,r2,r3,Reg_val,pc)

    elif opcode == "10010":
        r1 = instruction[5:8]
        imm = instruction[8:16]
        Move_I(r1,imm,Reg_val,pc)

    elif opcode == "10011":
        r1 = instruction[10:13]
        r2 = instruction[13:16]
        Move_R(r1,r2,Reg_val,pc)

    elif opcode == "10100":
        r1 = instruction[5:8]
        mem_add = b2d(instruction[8:16])
        Load(r1,mem_add,Memory,Reg_val,pc)

    elif opcode == "10101":
        r1 = instruction[5:8]
        mem_add = b2d(instruction[8:16])
        Store(r1,mem_add,Memory,Reg_val,pc)

    elif opcode == "10110":
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:16]
        Mul(r1,r2,r3,Reg_val,pc)

    elif opcode == "10111":
        r1 = instruction[10:13]
        r2 = instruction[13:16]
        Div(r1,r2,Reg_val,pc)

    elif opcode == "11000":
        r1 = instruction[5:8]
        imm = instruction[8:16]
        RightS(r1, imm,Reg_val,pc)

    elif opcode == "11001":
        r1 = instruction[5:8]
        imm = instruction[8:16]
        LeftS(r1,imm,Reg_val,pc)

    elif opcode == "11010":
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:16]
        XOR(r1,r2,r3,Reg_val,pc)

    elif opcode == "11011":
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:16]
        OR(r1,r2,r3,Reg_val,pc)

    elif opcode == "11100":
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:16]
        AND(r1,r2,r3,Reg_val,pc)

    elif opcode == "11101":
        r1 = instruction[10:13]
        r2 = instruction[13:16]
        Invert(r1,r2,Reg_val,pc)

    elif opcode == "11110":
        r1 = instruction[10:13]
        r2 = instruction[13:16]
        Compare(r1,r2,Reg_val,pc)

    elif opcode == "11111":
        mem_addr = instruction[8:16]
        U_Jump(mem_addr, pc, Reg_val)

    elif opcode == "01100":
        mem_addr = instruction[8:16]
        L_Jump(mem_addr, pc, Reg_val)

    elif opcode == "01101":
        mem_addr = instruction[8:16]
        G_Jump(mem_addr,pc,Reg_val)

    elif opcode == "01111":
        mem_addr = instruction[8:16]
        E_Jump(mem_addr,pc,Reg_val)

    elif opcode == "01010":
        Halt(halted,Reg_val,pc)

def main():
    Reg_val  = {"000":0, "001":0, "010":0, "011":0, "100":0, "101":0, "110":0, "111":0}
    Mem_dict = {}
    PC = 0
    Halted = False

    for i in range(0, 256):  # initialize the memory
        Mem_dict[i] = "0000000000000000"

    inst = 0  # read the input binary file and update the memory
    for line in sys.stdin:
        Mem_dict[inst] = line
        inst = inst + 1


    while Halted == False:
        instruction = Mem_dict[PC]
        Temp_pc  = PC
        driver(instruction,Reg_val,PC,Mem_dict,Halted)
        print((d2b(Temp_pc))[8:16], d2b(Reg_val["000"]), d2b(Reg_val["001"]), d2b(Reg_val["010"]),
              d2b(Reg_val["011"]), d2b(Reg_val["100"]), d2b(Reg_val["101"]), d2b(Reg_val["110"]),
              d2b(Reg_val["111"]))


    for i in Mem_dict:
        print(Mem_dict[i])



main()