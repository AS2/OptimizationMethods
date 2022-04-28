def parse_to_standart(A : list, b : list, c : list, v : float, limSigns : list, extrSign : str, valuesLimits : list):
    # init matrixes and vectors
    A_s = list()
    b_s = list()
    c_s = list()
    v_s = 0
    originalSize = len(c)
    originalVars = list()

    # first, remake target-function
    if extrSign == "min":
        c_s = [coef * -1 for coef in c]
        v_s = v * -1
    else:
        c_s = [coef for coef in c]
        v_s = v

    # second, correct all limits expressions
    for i in range(len(limSigns)):
        if limSigns[i] == "<=":
            A_s.append([A[i][j] for j in range(len(A[i]))])
            b_s.append(float(b[i]))
        elif limSigns[i] == ">=":
            A_s.append([A[i][j] * -1 for j in range(len(A[i]))])
            b_s.append(float(b[i]) * -1)
        elif limSigns[i] == "=":
            A_s.append([A[i][j] for j in range(len(A[i]))])
            b_s.append(float(b[i]))
            A_s.append([A[i][j] * -1 for j in range(len(A[i]))])
            b_s.append(float(b[i]) * -1)

    # finaly, correct if all variables have limit on thier sign
    for i in range(originalSize):
        if i not in valuesLimits:
            for A_line in A_s:
                A_line.append(A_line[i] * -1)
            c_s.append(-1 * c_s[i])
            originalVars.append([i, i, len(c_s) - 1])

    return A_s, b_s, c_s, v_s, originalSize, originalVars
