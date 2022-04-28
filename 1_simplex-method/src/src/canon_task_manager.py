from dual_task_manager import copyMatr, copyVec

def addSupportiveBasicValue(A : list, index : int, coef : float):
    for i in range(len(A)):
        if i == index:
            A[i].append(coef)
        else:
            A[i].append(0)
    return

def parse_to_canon(A : list, b : list, c : list, v : float, limSigns : list, extrSign : str, valuesLimits : list):
    # init matrixes and vectors
    A_c = copyMatr(A)
    b_c = copyVec(b)
    N = list()
    B = list()
    c_c = list()
    v_c = 0
    originalSize = len(c)
    originalVars = list()

    # first, remake target-function
    if extrSign == "max":
        c_c = [coef * -1 for coef in c]
        v_c = v * -1
    else:
        c_c = [coef for coef in c]
        v_c = v

    # second, correct all limits expressions
    for i in range(len(limSigns)):
        if limSigns[i] == "<=":
            B.append(len(c_c))
            addSupportiveBasicValue(A_c, i, 1)
            c_c.append(0)
        elif limSigns[i] == ">=":
            B.append(len(c_c))
            addSupportiveBasicValue(A_c, i, -1)
            c_c.append(0)

    # finaly, correct if all variables have limit on thier sign
    for i in range(originalSize):
        if i not in valuesLimits:
            for A_line in A_c:
                A_line.append(A_line[i] * -1)
            c_c.append(-1 * c_c[i])
            originalVars.append([i, i, len(c_c) - 1])

    for i in range(len(c_c)):
        if i not in B:
            N.append(i)
    return N, B, A_c, b_c, c_c, v_c, originalSize, originalVars

def print_task_as_canon(A : list, b : list, c : list, v : float):
    # BUILD TARGET FUNC
    str_to_out = "min: z = " + str(v)
    for i in range(len(c)):
        str_to_out += " + " + str(c[i]) + " * x" + str(i+1)
    print(str_to_out)

    # BUILD EXPRESSIONS
    for i in range(len(A)):
        str_to_out = str(b[i]) + " = "
        for j in range(len(A[i])):
            str_to_out += str(A[i][j]) + " * x" + str(j+1)
            if j != len(A[i]) - 1:
                str_to_out += " + "
        print(str_to_out)

    # BUILD VARIABLES
    str_to_out = ""
    for i in range(len(c)):
        if i != len(c) + len(A) - 1:
            str_to_out += "x" + str(i + 1) + ", "
        else:
            str_to_out += "x" + str(i + 1) + " >= 0"
            print(str_to_out)
    return

def convert_canon_solution_to_original(canon_sol : list, originalSize : int, originalVars : list):
    original_sol = list()
    original_indexes = [origVar[0] for origVar in originalVars]

    for i in range(originalSize):
        if i not in original_indexes:
            original_sol.append(canon_sol[i])
        else:
            for j in range(len(originalVars)):
                if i == originalVars[j][0]:
                    original_sol.append(canon_sol[originalVars[j][1]] - canon_sol[originalVars[j][2]])
    return original_sol
