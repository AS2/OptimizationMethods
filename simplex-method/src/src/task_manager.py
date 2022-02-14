from pathlib import Path

def read_task(filename : Path):
    # init matrixes and vectors
    A = list()
    b = list()
    limSigns = list()
    valuesLimits = list()
    wasSize = 0

    with open(filename, "r") as file:
        for line in file:
            if len(line.strip()) == 0 or (len(line.strip()) > 0 and line.strip()[0] == '#'):
                continue

            line_parts = line.split('=')

            if len(line_parts) != 2:
                return

            if line_parts[0].strip() == "n_size":
                wasSize = 1
                originalSize = int(line_parts[1].strip())
            elif wasSize == 1 and line_parts[0].strip() == "min_coef":
                if len(line_parts[1].strip().split(' ')) != originalSize:
                    return
                else:
                    extrSign = "min"
                    coefs_str = line_parts[1].strip().split(' ')
                    c = [float(coefs.strip())for coefs in coefs_str]
            elif wasSize == 1 and line_parts[0].strip() == "max_coef":
                if len(line_parts[1].strip().split(' ')) != originalSize:
                    return
                else:
                    extrSign = "max"
                    coefs_str = line_parts[1].strip().split(' ')
                    c = [float(coefs.strip()) for coefs in coefs_str]
            elif wasSize == 1 and line_parts[0].strip() == "free_coef":
                v = float(line_parts[1].strip())
            elif wasSize == 1 and line_parts[0].strip() == "equal":
                coefs_str = line_parts[1].strip().split(' ')

                if len(coefs_str) != originalSize + 1:
                    return

                A.append([float(coefs_str[i].strip()) for i in range(originalSize)])
                b.append(float(coefs_str[originalSize].strip()))
                limSigns.append("=")

            elif wasSize == 1 and line_parts[0].strip() == "more_equal":
                coefs_str = line_parts[1].strip().split(' ')

                if len(coefs_str) != originalSize + 1:
                    return

                A.append([float(coefs_str[i].strip()) for i in range(originalSize)])
                b.append(float(coefs_str[originalSize].strip()))
                limSigns.append(">=")

            elif wasSize == 1 and line_parts[0].strip() == "less_equal":
                coefs_str = line_parts[1].strip().split(' ')

                if len(coefs_str) != originalSize + 1:
                    return

                A.append([float(coefs_str[i].strip()) for i in range(originalSize)])
                b.append(float(coefs_str[originalSize].strip()))
                limSigns.append("<=")

            elif wasSize == 1 and line_parts[0].strip() == "not_neg_indexes":
                valuesLimits = [int(indx.strip()) for indx in line_parts[1].strip().split(' ')]
            else:
                return

    return A, b, c, v, limSigns, extrSign, valuesLimits
