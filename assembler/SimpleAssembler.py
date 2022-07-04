import sys

def readfile():
    counter = 0
    for line in sys.stdin:
        if line != "":
            counter = counter+1
            count = 0
            for i in range(len(line)):
                if line[i] == " ":
                    count = count +1
                else:
                    count = 0
                if count > 1 or line[i] == '\t':
                    listerror.append("invalid syntax error")
                    break
            listinp.append(line)

def check_number(s):
    for i in range(len(s)):
        if s[i].isdigit() != True:
            return False
    return True

def Label_Handling(input): #chckes for labels and halt

    halt = False
    counter = 0

    i = len(input)
    for j in range(0,i):
        split = input[j].split()
        if split[0] not in Opp_Dict and split[0] != "var":

            if split[0][-1] == ":":
                label_dict[split[0][:-1]] = counter
                counter = counter + 1

                if len(split) > 1:

                    if split[1] == "hlt":
                        halt = True
                        if j == (i-1):
                            return
                        else:
                            listerror.append("hlt is not at the end")
                            return
                # else:
                #     listerror.append("invalid syntax error")

            else:
                listerror.append("invalid syntax error")

        if split[0] == "hlt":
            halt = True
            if j == (i-1):
                return
            else:
                listerror.append("hlt is not at the end")
                return


    if halt == False:
        listerror.append("hlt is missing")

    return

def Variable_Handling(input): #Checks for variables
    counter = 0
    i = len(input)

    for j in range(0,i):
        split = input[j].split()
        if split[0] == "var":
            if len(split) == 2 and split[1] != "var":
                if j == counter:
                    var_dict[split[1]] = counter
                    counter = counter + 1
                else:
                    listerror.append("All variables must be defined at start")
            else:
                listerror.append("Invalid variable declaration")

def Register_Handling(reg): #Handles registers
    if reg in reg_add and reg != "FLAGS":
        return reg_add[reg]

    else:
        if reg == "FLAGS":
            listerror.append("Illegal use of FLAGS register")

        else:
            listerror.append("Invalid register value")

def d2b(num): #Converts decimal number to a binary number of 8 bits
    if (check_number(num) == True):
        s = bin(num).replace("0b", "")
        s = str(s)
        l = len(s)
        if len(s) < 8:
            for i in range(0,l):
                s = "0" + s

        return s

    else:
        listerror.append("Incorrect immediate value")



def Assembler(input): #the main assembler function
    for i in range (0, len(input)):
        binary = ""
        split = input[i].split()

        if split[0][:-1] in label_dict:
            split = split[1:]

        if len(split) > 0 and split[0] not in Opp_Dict and split[0] != "var":
            listerror.append("Invalid syntax error")

        if len(split) > 2 and split[0] == "mov" and split[2][0] == "$":
            Opp_Dict["mov"] = ("10010","B","2")

        else:
            Opp_Dict["mov"] = ("10011", "C","2")

        if len(split) > 0 and split[0] != "var" and split[0] in Opp_Dict:

            if len(split) == 4 and Opp_Dict[split[0]][1] == "A":
                binary = binary + Opp_Dict[split[0]][0] + "00"      #opcode and unesd bits

                for j in range(1,4):
                    reg = Register_Handling(split[j])
                    if reg:
                        binary = binary + reg

            elif len(split) == 3 and Opp_Dict[split[0]][1] == "B":
                binary = binary + Opp_Dict[split[0]][0]

                reg = Register_Handling(split[1],)
                if reg:
                    binary = binary + reg

                if int(split[2][1]) < 0 or int(split[2][1]) > 255:
                    listerror.append("Immediate value if out of bounds")
                else:
                    if (check_number(var_dict[split[2]]) == True):
                        o = d2b(split[2][1:])
                        binary = binary + o

            elif len(split) == 3 and Opp_Dict[split[0]][1] == "C":
                binary = binary + Opp_Dict[split[0]][0] + "00000"
                reg = Register_Handling(split[1])

                if reg:
                    binary = binary + reg

                if split[0] == "mov":
                    if split[2] in reg_add:
                        binary = binary + reg[split[2]]
                    else:
                        listerror.append("Invalid register value")

                else:
                    reg = Register_Handling(split[2])
                    if reg:
                        binary = binary + reg


            elif len(split) == 3 and Opp_Dict[split[0]][1] == "D":
                binary = binary + Opp_Dict[split[0]][0]
                reg = Register_Handling(split[1])

                if reg:
                    binary = binary + reg
                if split[2] in var_dict:
                    if(check_number(var_dict[split[2]]) == True):
                        o = d2b(int(var_dict[split[2]]))
                        binary = binary + o


                else:
                    if split[2] in label_dict:
                        listerror.append("label given where variable is required")
                    else:
                        listerror.append("Undefined variable")

            elif len(split) == 2 and Opp_Dict[split[0]][1] == "E":
                binary = binary + Opp_Dict[split[0]][0] + "000"

                if split[1] in label_dict:
                    if (check_number(var_dict[split[2]]) == True):
                        o = d2b(int(label_dict[split[1]]))
                        binary = binary + o

                else:
                    if split[1] in var_dict:
                        listerror.append("variable given where label is required")
                    else:
                        listerror.append("Undefined label")

            elif len(split) == 1 and Opp_Dict[split[0]][1] == "F":
                binary = binary + Opp_Dict[split[0]][0] + "00000000000"

            else:
                if split[0] in Opp_Dict:
                    listerror.append("Incorrectly parameters input")

        listout.append(binary)

    return


#Register Address
reg_add = {"R0":"000", "R1":"001" , "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}

#Operation Dictionary
Opp_Dict = {
    "add" : ("10000", "A","3"),
    "sub" : ("10001", "A","3"),
    "mov" : ("UNCLEAR","UNCLEAR","2"),
    "ld" : ("10100", "D","2"),
    "st" : ("10101", "D","2"),
    "mul" : ("10110", "A","3"),
    "div" : ("10111", "C","2"),
    "rs" : ("11000", "B","2"),
    "ls" : ("11001", "B","2"),
    "xor" : ("11010", "A","3"),
    "or" : ("11011", "A","3"),
    "and" : ("11100", "A","3"),
    "not" : ("11101", "C","2"),
    "cmp" : ("11110", "C","2"),
    "jmp" : ("11111", "E","1"),
    "jlt" : ("01100", "E","1"),
    "jgt" : ("01101", "E","1"),
    "je": ("01111", "E","1"),
    "hlt" : ("01010", "F","0")
}

#Variable Dictionary
var_dict ={}

#Label Dictionary
label_dict ={}

#output list with binaries
listout = []

#input list with instructions
listinp = []

#list of errors generated
listerror = []

def main():
    readfile()
    Label_Handling(listinp)
    Variable_Handling(listinp)
    Assembler(listinp)

    if len(listerror) == 0:
        for i in listout:
            print(i)

    else:
        for i in listerror:
            print(i)


main()