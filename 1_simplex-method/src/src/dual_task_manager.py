# theory source: https://matworld.ru/linear-programming/dvojstvennaja-zadacha.php

def copyMatr(A : list):
    A_copy = list()
    for i in range(len(A)):
        A_copy.append([A[i][j] for j in range(len(A[i]))])
    return A_copy

def copyVec(A : list):
    A_copy = list()
    for i in range(len(A)):
        A_copy.append(float(A[i]))
    return A_copy

def takeColumn(matrix : list, indx : int):
    return [matrix_line[indx] for matrix_line in matrix]

def parse_to_dual(A : list, b : list, c : list, v : float, limSigns : list, extrSign : str, valuesLimits : list):
    A_d = list()
    limSigns_d = list()
    valuesLimits_d = list()

    limitsCnt = len(limSigns)
    valuesCnt = len(c)

    A_tmp = copyMatr(A)

    # firstly, correct all limits expressions
    for i in range(limitsCnt):
        if (limSigns[i] == ">=" and extrSign == "max") or (limSigns[i] == "<=" and extrSign == "min"):
            if limSigns[i] == ">=":
                limSigns[i] = "<="
            else:
                limSigns[i] = ">="

            for j in range(len(A_tmp[i])):
                A_tmp[i][j] = -1 * A_tmp[i][j]
            b[i] = b[i] * -1

    # secondly, set dual target extremum
    if extrSign == "min":
        extrSign_d = "max"
        expr_d_sign = "<="
    else:
        extrSign_d = "min"
        expr_d_sign = ">="

    # thirdly, set dual target coefs
    c_d = b

    # fourtly, set limits free coefs
    b_d = c

    # fithly, set limits coefs
    for i in range(len(A_tmp[0])):
        A_d.append(takeColumn(A_tmp, i))

    # sixly, set limits signs
    for i in range(len(c)):
        if i in valuesLimits:
            limSigns_d.append(expr_d_sign)
        else:
            limSigns_d.append("=")

    # finaly, set values signs
    for i in range(limitsCnt):
        if limSigns[i] != "=":
            valuesLimits_d.append(i)

    v_d = 0
    return A_d, b_d, c_d, v_d, limSigns_d, extrSign_d, valuesLimits_d

def print_task_as_dual(A_d : list, b_d : list, c_d : list, v_d : float, limSigns_d : list, extrSign_d : str, valuesLimits_d : list):
    # BUILD TARGET FUNC
    str_to_out = extrSign_d + ": target = " + str(v_d)
    for i in range(len(c_d)):
        str_to_out += " + " + str(c_d[i]) + " * y" + str(i+1)
    print(str_to_out)

    # BUILD EXPRESSIONS
    for i in range(len(A_d)):
        str_to_out = ""
        for j in range(len(A_d[i])):
            str_to_out += str(A_d[i][j]) + " * y" + str(j+1)
            if j != len(A_d[i]) - 1:
                str_to_out += " + "
        str_to_out +=  " " + limSigns_d[i] + " " + str(b_d[i])
        print(str_to_out)

    # BUILD VARIABLES
    for i in range(len(c_d)):
        if i in valuesLimits_d:
            str_to_out = "y" + str(i+1) + " >= 0"
            print(str_to_out)

    return