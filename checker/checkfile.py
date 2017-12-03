def isSameString(s1, s2, chard = True, ccase = False, cfloat = False, precision = 6):
    l1 = str(s1).split()
    l2 = str(s2).split()
    if bool(chard):
        return l1 == l2


    if len(l1) != len(l2):
        return False

    res = True

    pre = pow(0.1, precision)

    for i in range(len(l1)):
        str1 = l1[i]
        str2 = l2[i]
        if bool(ccase):
            if (str1.lower() != str2.lower()):
                res = False

        if bool(cfloat):
            if (isfloat(str1) and isfloat(str2)):
                if (abs(float(str1) - float(str2)) > pre):
                    res = False
            else:
                res = False

        if not res:
            return res

    return res


def isSameFile(f1, f2, chard = True, ccase = False, cfloat = False, precision = 6):
    res = False
    try:
        file1 = open(f1, "r")
        file2 = open(f2, "r")
        s1 = file1.read()
        s2 = file2.read()
        file1.close()
        file2.close()
        res = isSameString(s1, s2, chard, ccase, cfloat, precision)
    except OSError:
        return False
    return res

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

