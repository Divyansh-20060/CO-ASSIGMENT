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
                    listerror["syntax error"] = counter
                    break
            listinp.append(line)





def Assembler(input, Opp_Dict):
    for i in range(0,len(input)):
        split = input[i].split()
        out = ""
        #if split[0] in Opp_Dict:




def Inst_Typo_Check(input,Opp_Dict): #input is a list of split instruction where input[0] is not var or a flag and does exist in OPP_Dict

    parmeters = len(input) - 1

    if(str(parmeters) != Opp_Dict[input][-1]):
        #handle inadequate parameters

    else:
        Type = Opp_Dict[input][1]

        if Type == "A":

        if Type == "B":

        if Type == "C":

        if Type == "D":

        if Type == "E":

        if Type == "F"




def Syntax_Errors(input):





#Register Address
reg_add = {"R0":"000", "R1":"001" , "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}

#Operation Dictionary
Opp_Dict = {
    "add" : ("00000", "A","3"),
    "sub" : ("00001", "A","3"),
    "mov" : ("UNCLEAR","UNCLEAR","2"),
    "ld" : ("00100", "D","2"),
    "st" : ("00101", "D","2"),
    "mul" : ("00110", "A","3"),
    "div" : ("00111", "C","2"),
    "rs" : ("01000", "B","2"),
    "ls" : ("01001", "B","2"),
    "xor" : ("01010", "A","3"),
    "or" : ("01011", "A","3"),
    "and" : ("01100", "A","3"),
    "not" : ("01101", "C","2"),
    "cmp" : ("01110", "C","2"),
    "jmp" : ("01111", "E","1"),
    "jlt" : ("10000", "E","1"),
    "jgt" : ("10001", "E","1"),
    "je": ("10010", "E","1"),
    "hlt" : ("10011", "F","0"),
    "var":("UNCLEAR","UNCLEAR","1")
}
my_dict={"add" : ("10000", 'A')}
f=open("pro.txt","r")
line=f.readline()
line_split=line.split()
#print(line_split)
if((line_split[0]=="ADD") and my_dict["add"][1]=='A'):
    x,y=int(line_split[1]),int(line_split[2])
    sum=x+y
    print(sum)
else:
    print("Invalid Instruction")


listout = []
listinp = []
listerror = []
