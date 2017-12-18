def isSameString(s1, s2, log, chard = True, ccase = False, cfloat = False, precision = 6):
    file = open(log, "w")

    l1 = str(s1).split()
    l2 = str(s2).split()
    while len(l1) < len(l2):
        l1.append("")
    if bool(chard):
        # return l1 == l2
        res = True
        for i in range(len(l2)):
            if l1[i] == l2[i]:
                file.write("1 ")
            else:
                res = False
                file.write("0 ")
        return res

    # if len(l1) != len(l2):
    #     for i in range(len(l2)):
    #         if l1[i] == l2[i]:
    #             file.write("1 ")
    #         else
    #             res = False
    #             file.write("0 ")
    #     return False

    res = True

    pre = pow(0.1, precision)

    for i in range(len(l2)):
        str1 = l1[i]
        str2 = l2[i]
        sam = True
        if bool(ccase):
            if (str1.lower() != str2.lower()):
                res = False
                sam = False

        if bool(cfloat):
            if (isfloat(str1) and isfloat(str2)):
                if (abs(float(str1) - float(str2)) > pre):
                    res = False
                    sam = False
            else:
                res = False
                sam = False

        if sam:
            file.write("1 ")
        else:
            file.write("0 ")

    file.close()
    return res


def isSameFile(f1, f2, log, chard = True, ccase = False, cfloat = False, precision = 6):
    res = False
    try:
        file1 = open(f1, "r")
        file2 = open(f2, "r")
        s1 = file1.read()
        s2 = file2.read()
        file1.close()
        file2.close()
        res = isSameString(s1, s2, log, chard, ccase, cfloat, precision)
    except OSError:
        return False
    return res

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

