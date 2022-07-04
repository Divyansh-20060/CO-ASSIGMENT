def d2b(num):
    s = bin(num).replace("0b", "")

    s = str(s)


    s = str(s)

    l = len(s)

    if len(s) < 8:
        for i in range(0,l):
            s = "0" + s

    return s

print(d2b(8))

listinp = ["var abc", "var var","add R0 R1 R2","ok: hlt"]

split = listinp[0].split()
print(split[0][:-1])