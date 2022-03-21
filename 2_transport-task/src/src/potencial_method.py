import numpy as np
from utils import *

import enum
import copy

class whereWasEnd(enum.Enum):
    NONE = -1
    HORZ = 0
    VERT = 1


# смотрим все непосещенные точки на горизонтали
def look_all_pos_on_horz(M : int, N : int, loopMap : list, pos_row : int,  pos_column : int):
    result = list()

    for j in range(0, N):
        if loopMap[pos_row][j][0] != IS_EMPTY and loopMap[pos_row][j][1] == -1 and j != pos_column:
            result.append([pos_row, j])

    return result

# смотрим все непосещенные точки на вертикали
def look_all_pos_on_vert(M : int, N : int, loopMap : list, pos_row : int,  pos_column : int):
    result = list()

    for i in range(0, M):
        if loopMap[i][pos_column][0] != IS_EMPTY and loopMap[i][pos_column][1] == -1 and i != pos_row:
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

# уходим в рекурсию для полного поиска всех циклов
def loop_recursion_all(M, N, loopMap, last_row, last_col, from_where, recursionLvl, allAnswers, currentLoop):
    loopMap[last_row][last_col][1] = recursionLvl
    currentLoop.append([last_row, last_col])

    # если оказались рядом с началом -> добавляем цикл
    if isThereLoopEndNear(M, N, loopMap, last_row, last_col, recursionLvl):
        allAnswers.append(copy.deepcopy(currentLoop))
    # если двигались не по горизонтали
    if from_where != whereWasEnd.HORZ:
        # ищем возможные циклы справа
        waysHorz = look_all_pos_on_horz(M, N, loopMap, last_row, last_col)
        for way in waysHorz:
            loop_recursion_all(M, N, loopMap, way[0], way[1], whereWasEnd.HORZ, recursionLvl + 1, allAnswers, currentLoop)

    # если двигались не по вертикали
    if from_where != whereWasEnd.VERT:
        # ищем возможные циклы сверху
        waysVert = look_all_pos_on_vert(M, N, loopMap, last_row, last_col)
        for way in waysVert:
            loop_recursion_all(M, N, loopMap, way[0], way[1], whereWasEnd.VERT, recursionLvl + 1, allAnswers, currentLoop)

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

    loop_recursion_all(M, N, loopMap, start_row, start_col, whereWasEnd.NONE, 0, allAnswers, currentLoop)
    smallestLoop = select_smallest_loop(allAnswers)

    return smallestLoop

# уходим в рекурсию чтоб искать наименьший цикл
def loop_recursion_smallest(M, N, loopMap, last_row, last_col, from_where, recursionLvl, smallestLoop, currentLoop):
    loopMap[last_row][last_col][1] = recursionLvl
    currentLoop.append([last_row, last_col])

    # если оказались рядом с началом -> добавляем цикл
    if isThereLoopEndNear(M, N, loopMap, last_row, last_col, recursionLvl) and ((len(smallestLoop) != 0 and len(smallestLoop) > len(currentLoop)) or len(smallestLoop) == 0):
        smallestLoop.clear()
        for block in currentLoop:
            smallestLoop.append(block)

    elif ((len(smallestLoop) != 0 and len(smallestLoop) > recursionLvl) or len(smallestLoop) == 0):
       # если двигались не по горизонтали
        if from_where != whereWasEnd.HORZ:
            # ищем возможные циклы справ
            waysHorz = look_all_pos_on_horz(M, N, loopMap, last_row, last_col)
            for way in waysHorz:
                loop_recursion_smallest(M, N, loopMap, way[0], way[1], whereWasEnd.HORZ, recursionLvl + 1, smallestLoop, currentLoop)

        # если двигались не по вертикали
        if from_where != whereWasEnd.VERT:
            # ищем возможные циклы сверху
            waysVert = look_all_pos_on_vert(M, N, loopMap, last_row, last_col)
            for way in waysVert:
                loop_recursion_smallest(M, N, loopMap, way[0], way[1], whereWasEnd.VERT, recursionLvl + 1, smallestLoop, currentLoop)

    # все поиски закончены -> зачищаем свое наличие в карте и в текущем рассматриваемом цикле
    loopMap[last_row][last_col][1] = -1
    currentLoop.pop(len(currentLoop) - 1)
    return

# функция старта поиска всех циклов. Здесь строим начальные вспомогательные данные, затем просто обходим рекурсивно абсолютно все возможные варианты пока не найдем цикл
def find_smallest_loop(M : int, N : int, plan : list, start_row : int, start_col : int):
    # создаем двумерны массив пар вида (клетка начального плана, номер шага в рассматриваемом пути)
    loopMap = [[[plan[i][j], -1] for j in range(N)] for i in range(M)]
    smallestLoop = list()
    currentLoop = list()
    loop_recursion_smallest(M, N, loopMap, start_row, start_col, whereWasEnd.NONE, 0, smallestLoop, currentLoop)
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

# решение транспортной задачи методом потенциалов
def potencial_solution(M : int, N : int, m_count : list, n_count : list, coefs : list, printIters : bool):
    plan = north_west_corner_rule(M, N, m_count, n_count)

    newPoint = isPlanOptimal(M, N, m_count, n_count, coefs, plan)
    iter = 0
    while len(newPoint) != 0:
        loop = find_smallest_loop(M, N, plan, newPoint[0], newPoint[1])
        if printIters == True:
            print_iter(loop, plan, iter)
            iter += 1
        plan = rewrite_plan(M, N, plan, loop)
        newPoint = isPlanOptimal(M, N, m_count, n_count, coefs, plan)

    return convert_into_ready_plan(M, N, plan)
