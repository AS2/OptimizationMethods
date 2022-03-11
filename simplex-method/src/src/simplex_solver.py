import copy

EPS = 0.000000001

def min_index(delta: list, B: list):
    for index, value in enumerate(delta):
        if index not in B:
            continue
        minimum = value
        minimum_index = index
        
        if minimum != "inf":
            break
    if minimum == "inf":
        return minimum_index
    for index, value in enumerate(delta):
        if index not in B:
            continue
        if value == "inf":
            continue
        if value < minimum:
            minimum = value
            minimum_index = index

    return minimum_index

def init_simplex(A, b, c):
    # СОЗДАНИЕ РАСШИРЕННЫХ МАТРИЦ И ВЕКТОРОВ РАЗМЕРАМИ (m + n) x (m + n) и (m + n) x 1
    # ДЛЯ БОЛЕЕ УДОБНОГО ОПЕРИРОВАНИЯ ЧИСЛАМИ
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

    # ПРОВЕРКА НА НАЛИЧИЕ НАЧАЛЬНОГО БАЗИСНОГО РЕШЕНИЯ
    k = b.index(min(b))
    if b[k] > 0:
        return N, B, new_A, new_b, c, 0

    new_b.insert(0, 0)
    new_A.insert(0, [0 for j in range(rows + cols)])
    for i in range(cols + rows + 1):
        if i < cols + 1:
            new_A[i].insert(0, 0)
        else:
            new_A[i].insert(0, -1)

    c_tmp = [0 if ind != 0 else -1 for ind in range(rows + cols + 1)]
    v_tmp = 0
    N_tmp = [i for i in range(cols + 1)]
    B_tmp = [cols + 1 + i for i in range(rows)]

    l = cols + k + 1

    N_tmp, B_tmp, new_A, new_b, c_tmp, v_tmp = pivot(N_tmp, B_tmp, new_A, new_b, c_tmp, v_tmp, l, 0)

    x_opt = list()
    while(max(c_tmp) > EPS):
        N_tmp, B_tmp, new_A, new_b, c_tmp, v_tmp = simplex_iteration(N_tmp, B_tmp, new_A, new_b, c_tmp, v_tmp)
        
    for i in range(len(new_A)):
        if i in B_tmp:
            x_opt.append(new_b[i])
        else:
            x_opt.append(0)

    if abs(x_opt[0]) < EPS:
        # ЕСЛИ Х0 - БАЗИСНАЯ, ТО ЗАМЕЩАЕМ ЕЕ ЧТОБ СТАЛА НЕБАЗИСНОЙ
        if 0 in B_tmp:
            e_tmp = -1
            for i in N_tmp:
                if abs(new_A[0][i]) > EPS:
                    e_tmp = i
            N_tmp, B_tmp, new_A, new_b, c_tmp, v_tmp = pivot(N_tmp, B_tmp, new_A, new_b, c_tmp, v_tmp, 0, e_tmp)

        # КОГДА Х0 - НЕБАЗИСНАЯ, ВОССТАНАВЛИВАЕМ ЦЕЛЕВУЮ ФУНКУИЮ И УБИРАЕМ Х0 ИЗ ОГРАНИЧЕНИЙ
        # чистим матрицу ограничений c свободными членами
        new_b.pop(0)
        new_A.pop(0)
        for i in range(cols + rows):
            new_A[i].pop(0)
        # понижаем индексы в N_tmp и B_tmp на 1
        N_tmp.remove(0)
        for i in range(len(N_tmp)):
            N_tmp[i] = N_tmp[i] - 1
        for i in range(len(B_tmp)):
            B_tmp[i] = B_tmp[i] - 1

        # восстанавливаем целевую функцию
        v_res = 0
        for i in range(cols):
            if i in B_tmp:
                coef_tmp = c[i]
                v_res += coef_tmp * new_b[i]
                for j in range(rows + cols):
                    if j != i:
                        c[j] -= coef_tmp * new_A[i][j]
                    else:
                        c[i] = 0.0

        return N_tmp, B_tmp, new_A, new_b, c, v_res
    else:
        raise Exception("Задача неразрешима")


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

def simplex_iteration(N: list, B: list, A: list, b: list, c: list, v: int):
    delta = [0 for m in range(len(A))]
    N.sort()
    B.sort()

    e = -1
    for j in N:
        if c[j] > EPS:
            # ПРАВИЛО БЛЕНДА : ВЫБИРАЕМ НАИМЕНЬШИЙ ИНДЕКС НЕБАЗИСНОГО ЭЛЕМЕНТА НА ВХОД
            if (e != -1 and j < e) or e == -1:
                e = j

    for i in B:
        if A[i][e] > EPS:
            delta[i] = b[i] / A[i][e]
        else:
            delta[i] = "inf"
    
    l = min_index(delta, B)
    if delta[l] == "inf":
        raise Exception("Задача не ограничена")
    else:
        N, B, A, b, c, v = pivot(N, B, A, b, c, v, l, e)

    return N, B, A, b, c, v

def simplex(N: list, B: list, A: list, b: list, c: list, v: int):
    x = list()

    while(max(c) > EPS):
        N, B, A, b, c, v = simplex_iteration(N, B, A, b, c, v)
        
    for i in range(len(A)):
        if i in B:
            x.append(b[i])
        else:
            x.append(0)
    
    return x
