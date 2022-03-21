import numpy as np

import copy

IS_EMPTY = -1

def make_task_close(M : int, N : int, m_count : list, n_count : list, coefs : list):
    sum_cons = sum(n_count)
    sum_prov = sum(m_count)
    
    # если предоставляем больше, чем нужно -> добавляем фиктивного потребителя
    if (sum_cons < sum_prov):
        print("В введенной задаче предоставляем больше, чем нужно -> добавляем фиктивного потребителя")
        for coef_row in coefs:
            coef_row.append(0)
        N = N + 1
        n_count.append(sum_prov - sum_cons)
    # если предоставляем меньше, чем нужно -> добавляем фиктивного поставщика
    elif (sum_cons > sum_prov):
        print("В введенной задаче предоставляем меньше, чем нужно -> добавляем фиктивного поставщика")
        coefs.append([0 for i in range(N)])
        M = M + 1
        m_count.append(sum_cons - sum_prov)
    else:
        print("Введенная задача закрыта")
    return M, N, m_count, n_count, coefs



def to_canon(M : int, N : int, m_count : list, n_count : list, coefs : list):
    min_task = list()
    for i in range(M):
        for j in range(N):
            min_task.append(int(coefs[i][j]))

    b_vec = [m_count[i] if i < M else n_count[i - M] for i in range(M + N)]
    A_matr = [[0 for i in range(M * N)] for i in range (M + N)]

    # заполняем строки-ограничения на поставку
    for i in range(M):
        for j in range(N):
            A_matr[i][i * N + j] = 1

    # заполняем строки-ограничения на прием
    for i in range(N):
        for j in range(M):
            A_matr[M + i][i + j * N] = 1

    return min_task, A_matr, b_vec

def north_west_corner_rule(M : int, N : int, m_count : list, n_count : list):
    # "-1" - поставок нет, "0" - поставляются 0 припасов 
    # (тип поставка есть, но ничего не поставляют, как бы пустой грузовик едет)
    solution = [[IS_EMPTY for j in range(N)] for i in range(M)]
    northest_row = 0
    m_count_tmp = [m_count[i] for i in range(M)]
    n_count_tmp = [n_count[i] for i in range(N)]

    for i in range(N):
        for j in range(northest_row, M):
            count = min(m_count_tmp[j], n_count_tmp[i])
            if count > 0:
                solution[j][i] = count
                m_count_tmp[j] = m_count_tmp[j] - count
                n_count_tmp[i] = n_count_tmp[i] - count
                if m_count_tmp[j] == 0 and n_count_tmp[i] != 0:
                    northest_row = j + 1
                elif m_count_tmp[j] != 0 and n_count_tmp[i] == 0:
                    break
                elif m_count_tmp[j] == 0 and n_count_tmp[i] == 0 and (j != M - 1 or i != N - 1):
                    if j != M - 1:
                        solution[j + 1][i] = 0
                    elif j != N - 1:
                        solution[j][i + 1] = 0

    return solution

# функция вывода циклов
def print_iter(loop : list, plan : list, iter : int):
    print("Iteration #" + str(iter))

    strLoop = "(" + str(loop[0][0]) + ", " + str(loop[0][1]) + ")"
    for i in range(1, len(loop)):
        strLoop += " -> (" + str(loop[i][0]) + ", " + str(loop[i][1]) + ")"
    print(strLoop)

    for i in range(len(plan)):
        rowToPrint = [str(plan[i][j]) if plan[i][j] != IS_EMPTY else "*" for j in range(len(plan[0]))]
        print(rowToPrint)
    return

# функция вывода ответа
def print_result(plan : list, coefs : list):
    print("Итого наилучший план")
    for i in range(len(plan)):
        rowToPrint = [str(plan[i][j]) if plan[i][j] != IS_EMPTY else "*" for j in range(len(plan[0]))]
        print(rowToPrint)

    res = 0
    for i in range(len(plan)):
        for j in range(len(plan[0])):
            res += plan[i][j] * coefs[i][j]
    print("Итоговая стоимость: " + str(res))
    return

# функция перевода плана в удобный для понимания вид
def convert_into_ready_plan(M : int, N : int, plan : list):
    for i in range(M):
        for j in range(N):
            if plan[i][j] == IS_EMPTY:
                plan[i][j] = 0
    return plan

# расчет потенциалов
def get_potencials(M : int, N : int, plan : list, coefs : list):
    # находим потенциалы
    u = [0 for i in range(M)]
    v = [0 for j in range(N)]

    # делаем СЛАУ и решаем при помоще np.solve
    A = [[0 for j in range(N + M)] for i in range(N + M)]
    b = [0 for i in range(N + M)]

    A[0][0] = 1
    b[0] = 0
    var = 1
    for i in range(M):
        for j in range(N):
            if plan[i][j] != IS_EMPTY:
                A[var][i] = -1
                A[var][M + j] = 1
                b[var] = coefs[i][j]
                var = var + 1
    x = np.linalg.solve(A, b)
    for i in range(M + N):
        if i < M:
            u[i] = x[i]
        else:
            v[i - M] = x[i]

    return u, v

# проверка на оптимальность - если возвращается пустой массив - то решение оптимально,
# иначе возвращается массив из двух элементов - координаты точки (row, column), с которой нужно будет строить цикл
def isPlanOptimal(M : int, N : int, m_count : list, n_count : list, coefs : list, plan : list):
    u, v = get_potencials(M, N, plan,  coefs)

    hugestDelta = -1
    newPoint = []
    for i in range(M):
        for j in range(N):
            if plan[i][j] == IS_EMPTY and v[j] - u[i] > coefs[i][j]:
                if v[j] - u[i] - coefs[i][j] > hugestDelta:
                    newPoint = [i, j]
                    hugestDelta = v[j] - u[i] - coefs[i][j]


    return newPoint

def toTmp(plan : list):
    for i in range(len(plan)):
        for j in range(len(plan[0])):
            if plan[i][j] == 0:
                plan[i][j] = IS_EMPTY
    return plan