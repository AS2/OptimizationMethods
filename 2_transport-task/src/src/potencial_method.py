import numpy as np
from utils import *

import enum
import copy

class whereWasEnd(enum.Enum):
    ONLY_STARTED = -1
    WENT_FROM_LEFT = 0
    WENT_FROM_BOTTOM = 1
    WENT_FROM_RIGHT = 2
    WENT_FROM_TOP = 3


# смотрим все непосещенные точки справа
def look_all_pos_from_right(M : int, N : int, loopMap : list, pos_row : int,  pos_column : int):
    result = list()

    for j in range(pos_column + 1, N):
        if loopMap[pos_row][j][0] != IS_EMPTY and loopMap[pos_row][j][1] == -1:
            result.append([pos_row, j])

    return result

# смотрим все непосещенные точки слева
def look_all_pos_from_left(M : int, N : int, loopMap : list, pos_row : int,  pos_column : int):
    result = list()

    for j in range(0, pos_column):
        if loopMap[pos_row][j][0] != IS_EMPTY and loopMap[pos_row][j][1] == -1:
            result.append([pos_row, j])

    return result

# смотрим все непосещенные точки снизу
def look_all_pos_from_bottom(M : int, N : int, loopMap : list, pos_row : int,  pos_column : int):
    result = list()

    for i in range(pos_row + 1, M):
        if loopMap[i][pos_column][0] != IS_EMPTY and loopMap[i][pos_column][1] == -1:
            result.append([i, pos_column])

    return result

# смотрим все непосещенные точки снизу
def look_all_pos_from_top(M : int, N : int, loopMap : list, pos_row : int,  pos_column : int):
    result = list()

    for i in range(0, pos_row):
        if loopMap[i][pos_column][0] != IS_EMPTY and loopMap[i][pos_column][1] == -1:
            result.append([i, pos_column])

    return result

# функция проверки, нет ли случаем где то в строке или в столбце нуля? Если есть - вернем True, иначе False
def isThereLoopEndNear(M : int, N : int, loopMap : list, pos_row : int, pos_column : int, recursionLvl : int):
    if recursionLvl < 3:
        return False

    for i in range(N):
        if loopMap[pos_row][i][1] == 0 and i != pos_column:
            return True

    for i in range(M):
        if loopMap[i][pos_column][1] == 0 and i != pos_row:
            return True

    return False

# берем самый короткий из циклов
def select_smallest_loop(allLoops : list):
    if len(allLoops) == 0:
        return []

    smallestLoop = allLoops[0]
    for loop in allLoops:
        if len(loop) < len(smallestLoop):
            smallestLoop = loop

    return smallestLoop

# уходим в рекурсию
def loop_recursion(M, N, loopMap, last_row, last_col, from_where, recursionLvl, allAnswers, currentLoop):
    loopMap[last_row][last_col][1] = recursionLvl
    currentLoop.append([last_row, last_col])

    # если оказались рядом с началом -> добавляем цикл
    if isThereLoopEndNear(M, N, loopMap, last_row, last_col, recursionLvl):
        allAnswers.append(copy.deepcopy(currentLoop))
    else:
        # ищем возможные циклы справа
        if from_where != whereWasEnd.WENT_FROM_RIGHT and from_where != whereWasEnd.WENT_FROM_LEFT:
            waysFromRight = look_all_pos_from_right(M, N, loopMap, last_row, last_col)
            for way in waysFromRight:
                loop_recursion(M, N, loopMap, way[0], way[1], whereWasEnd.WENT_FROM_RIGHT, recursionLvl + 1, allAnswers, currentLoop)
        # ищем возможные циклы слева
        if from_where != whereWasEnd.WENT_FROM_RIGHT and from_where != whereWasEnd.WENT_FROM_LEFT:
            waysFromLeft = look_all_pos_from_left(M, N, loopMap, last_row, last_col)
            for way in waysFromLeft:
                loop_recursion(M, N, loopMap, way[0], way[1], whereWasEnd.WENT_FROM_LEFT, recursionLvl + 1, allAnswers, currentLoop)
        # ищем возможные циклы сверху
        if from_where != whereWasEnd.WENT_FROM_TOP and from_where != whereWasEnd.WENT_FROM_BOTTOM:
            waysFromTop = look_all_pos_from_top(M, N, loopMap, last_row, last_col)
            for way in waysFromTop:
                loop_recursion(M, N, loopMap, way[0], way[1], whereWasEnd.WENT_FROM_TOP, recursionLvl + 1, allAnswers, currentLoop)
        # ищем возможные циклы справа
        if from_where != whereWasEnd.WENT_FROM_TOP and from_where != whereWasEnd.WENT_FROM_BOTTOM:
            waysFromBottom = look_all_pos_from_bottom(M, N, loopMap, last_row, last_col)
            for way in waysFromBottom:
                loop_recursion(M, N, loopMap, way[0], way[1], whereWasEnd.WENT_FROM_BOTTOM, recursionLvl + 1, allAnswers, currentLoop)

    # все поиски закончены -> зачищаем свое наличие в карте и в текущем рассматриваемом цикле
    loopMap[last_row][last_col][1] = -1
    currentLoop.pop(len(currentLoop) - 1)
    return

# функция старта поиска всех циклов. Здесь строим начальные вспомогательные данные, затем просто обходим рекурсивно абсолютно все возможные варианты пока не найдем цикл
def find_all_loops(M : int, N : int, plan : list, start_row : int, start_col : int):
    # создаем двумерны массив пар вида (клетка начального плана, номер шага в рассматриваемом пути)
    loopMap = [[[plan[i][j], -1] for j in range(N)] for i in range(M)]
    allAnswers = list()

    currentLoop = list()
    #currentLoop.append((start_x, start_y))
    loop_recursion(M, N, loopMap, start_row, start_col, whereWasEnd.ONLY_STARTED, 0, allAnswers, currentLoop)
    smallestLoop = select_smallest_loop(allAnswers)

    return smallestLoop

# находим минимальную поставку в цикле
def minimum_in_loop(plan : list, loop : list):
    min = 999999999
    for i in range(len(loop)):
        if plan[loop[i][0]][loop[i][1]] < min and plan[loop[i][0]][loop[i][1]] != IS_EMPTY and i % 2 == 1:
            min = plan[loop[i][0]][loop[i][1]]
    return min

# переписываем план поставок
def rewrite_plan(M : int, N : int, plan : list, loop : list):
    sign = 1
    index = 0
    min = minimum_in_loop(plan, loop)

    wasNewZero = False
    while index != len(loop):
        if plan[loop[index][0]][loop[index][1]] == IS_EMPTY:
            plan[loop[index][0]][loop[index][1]] = min
        else:
            plan[loop[index][0]][loop[index][1]] = plan[loop[index][0]][loop[index][1]] + sign * min
            if plan[loop[index][0]][loop[index][1]] == 0 and wasNewZero == False:
                wasNewZero = True
                plan[loop[index][0]][loop[index][1]] = IS_EMPTY
        sign = sign * -1
        index = index + 1

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
                A[var][i] = 1
                A[var][M + j] = -1
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
            if plan[i][j] == IS_EMPTY and u[i] - v[j] > coefs[i][j]:
                if u[i] - v[j] - coefs[i][j] > hugestDelta:
                    newPoint = [i, j]
                    hugestDelta = u[i] - v[j] - coefs[i][j]


    return newPoint

# решение транспортной задачи методом потенциалов
def potencial_solution(M : int, N : int, m_count : list, n_count : list, coefs : list, printIters : bool):
    plan = north_west_corner_rule(M, N, m_count, n_count)

    newPoint = isPlanOptimal(M, N, m_count, n_count, coefs, plan)
    iter = 0
    while len(newPoint) != 0:
        loop = find_all_loops(M, N, plan, newPoint[0], newPoint[1])
        if printIters == True:
            print_iter(loop, plan, iter)
            iter += 1
        plan = rewrite_plan(M, N, plan, loop)
        newPoint = isPlanOptimal(M, N, m_count, n_count, coefs, plan)

    return convert_into_ready_plan(M, N, plan)
