def cormens_parse_to_canon(A : list, b : list, c : list, v : float, limSigns : list, extrSign : str, valuesLimits : list):
    # init matrixes and vectors
    A_c = list()
    b_c = list()
    c_c = list()
    v_c = 0
    originalSize = len(c)
    originalVars = list()

    # first, remake target-function
    if extrSign == "min":
        c_c = [coef * -1 for coef in c]
        v_c = v * -1
    else:
        c_c = [coef for coef in c]
        v_c = v

    # second, correct all limits expressions
    for i in range(len(limSigns)):
        if limSigns[i] == "<=":
            A_c.append([A[i][j] for j in range(len(A[i]))])
            b_c.append(float(b[i]))
        elif limSigns[i] == ">=":
            A_c.append([A[i][j] * -1 for j in range(len(A[i]))])
            b_c.append(float(b[i]) * -1)
        elif limSigns[i] == "=":
            A_c.append([A[i][j] for j in range(len(A[i]))])
            b_c.append(float(b[i]))
            A_c.append([A[i][j] * -1 for j in range(len(A[i]))])
            b_c.append(float(b[i]) * -1)

    # finaly, correct if all variables have limit on thier sign
    for i in range(originalSize):
        if i not in valuesLimits:
            for A_line in A_c:
                A_line.append(A_line[i] * -1)
            c_c.append(-1 * c_c[i])
            originalVars.append([i, i, len(c_c) - 1])

    return A_c, b_c, c_c, v_c, originalSize, originalVars

def cormen_print_task_as_canon(A : list, b : list, c : list, v : float):
    # BUILD TARGET FUNC
    str_to_out = "max: z = " + str(v)
    for i in range(len(c)):
        str_to_out += " + " + str(c[i]) + " * x" + str(i+1)
    print(str_to_out)

    # BUILD EXPRESSIONS
    for i in range(len(A)):
        str_to_out = "x" + str(len(c) + i + 1) + " = " + str(b[i])
        for j in range(len(A[i])):
            str_to_out += " - " + str(A[i][j]) + " * x" + str(j+1)
        print(str_to_out)

    # BUILD VARIABLES
    str_to_out = ""
    for i in range(len(c) + len(A)):
        if i != len(c) + len(A) - 1:
            str_to_out += "x" + str(i + 1) + ", "
        else:
            str_to_out += "x" + str(i + 1) + " >= 0"
            print(str_to_out)
    return
