import sys

def readfile():
    counter = 0
    for line in sys.stdin:
        if line != "":
            counter = counter+1
            count = 0
            for i in range(0,len(line)):
                if line[i] == " ":
                    count = count +1
                else:
                    count = 0
                if count > 1 or line[i] == '\t':
                    listerror["syntax error"] = counter
                    break
            listinp.append(line)



listinp = []
listerror = []