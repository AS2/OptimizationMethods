import copy

def min_index(delta: list, B: list):
    for index, value in enumerate(delta):
        if index not in B:
            continue
        mininum = value
        mininum_index = index

        if mininum != "inf":
            break;
    if mininum == "inf":
        return mininum_index
    for index, value in enumerate(delta):
        if index not in B:
            continue
        if value == "inf":
            continue
        if value < mininum:
            minimum = value
            mininum_index = index
    return mininum_index

def init_simplex(A, b, c):
    rows = len(A)
    cols = len(A[0])

    N = [i for i in range(cols)]
    B = [cols + i for i in range(rows)]
    c = [c[idx] if idx < len(c) else 0 for idx in range(rows + cols)]
    new_b = [0 if idx < cols else b[idx - cols] for idx in range(rows + cols)]
    new_A = [[0 for j in range(rows + cols)] for i in range(rows + cols)]
    
    for i in range(rows):
        for j in range(cols):
            new_A[i + cols][j] = A[i][j]

    return N, B, new_A, new_b, c, 0

def pivot(N: list, B: list, A: list, b: list, c: list, v: int, l: int, e: int):
    N_new = copy.deepcopy(N)
    B_new = copy.deepcopy(B)
    A_new = [[0 for i in range(len(A[0]))] for j in range(len(A))]
    b_new = [0 for i in range(len(b))]
    c_new = [0 for i in range(len(c))]

    b_new[e] = b[l] / A[l][e]

    for j in N:
        if j != e:
            A_new[e][j] = A[l][j] / A[l][e]
    A_new[e][l] = 1 / A[l][e]

    for i in B:
        if i != l:
            b_new[i] = b[i] - A[i][e] * b_new[e]

            for j in N:
                if j != e:
                    A_new[i][j] = A[i][j] - A[i][e] * A_new[e][j]
            
            A_new[i][l] = -A[i][e] * A_new[e][l]
    
    v_new = v + c[e] * b_new[e]

    for j in N:
        if j != e:
            c_new[j] = c[j] - c[e] * A_new[e][j]
    c_new[l] = -c[e] * A_new[e][l]

    if e in N:
        N_new.remove(e)
    N_new.append(l)

    if l in B:
        B_new.remove(l)
    B_new.append(e)

    return N_new, B_new, A_new, b_new, c_new, v_new

def simplex(N: list, B: list, A: list, b: list, c: list, v: int):
    x = list()

    while(True):
        delta = [0 for m in range(len(A))]

        e = -1
        for j in N:
            if c[j] > 0:
                e = j
        if e == -1:
            break
                
        for i in B:
            if A[i][e] > 0:
                delta[i] = b[i] / A[i][e]
            else:
                delta[i] = "inf"
        
        l = min_index(delta, B)
        if delta[l] == "inf":
            raise Exception("Задача не ограничена")
        else:
            N, B, A, b, c, v = pivot(N, B, A, b, c, v, l, e)
        
    for i in range(len(A)):
        if i in B:
            x.append(b[i])
        else:
            x.append(0)
    
    return x