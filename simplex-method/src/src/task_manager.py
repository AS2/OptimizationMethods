from pathlib import Path

def read_task_as_canon(filename : Path):
    # init matrixes and vectors
    A = list()
    b = list()
    originalVars = list()

    with open(filename, "r") as file:
        for line in file:
            line_parts = line.split('=')

            if len(line_parts) != 2:
                return

            if line_parts[0].strip() == "n_size":
                originalSize = int(line_parts[1].strip())
            elif line_parts[0].strip() == "min_coef":
                if len(line_parts[1].strip().split(' ')) != originalSize:
                    return
                else:
                    coefs_str = line_parts[1].strip().split(' ')
                    c = [float(coefs.strip()) for coefs in coefs_str]
            elif line_parts[0].strip() == "min_freeValue":
                v = float(line_parts[1].strip())
            elif line_parts[0].strip() == "equal":
                coefs_str = line_parts[1].strip().split(' ')

                if len(coefs_str) != originalSize + 1:
                    return

                coefs_less = list()
                coefs_more = list()
                for i in range(originalSize):
                    coefs_less.append(float(coefs_str[i].strip()))
                    coefs_more.append(float(coefs_str[i].strip()) * -1)
                A.append(coefs_less)
                A.append(coefs_more)
                b.append(float(coefs_str[originalSize].strip()))
                b.append(float(coefs_str[originalSize].strip()) * -1)

            elif line_parts[0].strip() == "more_equal":
                coefs_str = line_parts[1].strip().split(' ')

                if len(coefs_str) != originalSize + 1:
                    return

                coefs_more = list()
                for i in range(originalSize):
                    coefs_more.append(float(coefs_str[i].strip()) * -1)
                A.append(coefs_more)
                b.append(float(coefs_str[originalSize].strip()))

            elif line_parts[0].strip() == "less_equal":
                coefs_str = line_parts[1].strip().split(' ')

                if len(coefs_str) != originalSize + 1:
                    return

                coefs_less = list()
                for i in range(originalSize):
                    coefs_less.append(float(coefs_str[i].strip()))
                A.append(coefs_less)
                b.append(float(coefs_str[originalSize].strip()))

            elif line_parts[0].strip() == "not_neg_indexes":
                neg_indexes = [int(indx.strip()) for indx in line_parts[1].strip().split(' ')]

                for i in range(originalSize):
                    if i not in neg_indexes:
                        for A_line in A:
                            A_line.append(A_line[i] * -1)
                        c.append(-1 * c[i])
                        originalVars.append([i, i, originalSize + i])
            else:
                return

    return A, b, c, v, originalSize, originalVars

def print_task_as_canon(A : list, b : list, c : list, v : float):
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
    return

def convert_canon_solution_to_original(canon_sol : list, originalSize : int, originalVars : list):
    original_sol = list()
    original_indexes = [origVar[0] for origVar in originalVars]

    for i in range(originalSize):
        if i not in original_indexes:
            original_sol.append(canon_sol[i])
        else:
            for j in range(originalVars):
                if i == origin_indexes[j][0]:
                    original_sol.append(canon_sol[originalVars[j][1]] - canon_sol[originalVars[j][2]])
    return original_sol


def getSomeColumn(matrix : list, columnIdx : int):
    column = [row[columnIdx] for row in matrix]
    return column
