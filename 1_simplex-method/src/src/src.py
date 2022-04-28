import numpy as np

from task_manager import read_task
from standart_task_manager import parse_to_standart
from canon_task_manager import parse_to_canon, print_task_as_canon, convert_canon_solution_to_original
from dual_task_manager import parse_to_dual, print_task_as_dual
from brute_force import solve_brute_force
from simplex_solver import simplex
from simplex_solver import init_simplex

A, b, c, v, limSigns, extrSign, valuesLimits = read_task("task.txt")

N_c, B_c, A_c, b_c, c_c, v_c, origSize_c, origVar_c = parse_to_canon(A, b, c, v, limSigns, extrSign, valuesLimits)
print("-= CANON TASK =-")
print_task_as_canon(A_c, b_c, c_c, v_c)
print("solution:")
solution = convert_canon_solution_to_original(solve_brute_force(A_c, b_c, c_c, v_c), origSize_c, origVar_c)
print(solution)
print(np.dot(solution, c))
# МЕСТО ПОД РЕШЕНИЕ СИМПЛЕКСОМ
A_std, b_std, c_std, v_std, origSize_std, origVar_std = parse_to_standart(A, b, c, v, limSigns, extrSign, valuesLimits)
N_s, B_s, A_s, b_s, c_s, v_s = init_simplex(A_std, b_std, c_std)
print("simplex solution:")
solution = convert_canon_solution_to_original(simplex(N_s, B_s, A_s, b_s, c_s, v_s), origSize_std, origVar_std)
print(solution)
print(np.dot(solution, c))


A_d, b_d, c_d, v_d, limSigns_d, extrSign_d, valuesLimits_d = parse_to_dual(A, b, c, v, limSigns, extrSign, valuesLimits)
print("-= DUAL TASK =-")

print_task_as_dual(A_d, b_d, c_d, v_d, limSigns_d, extrSign_d, valuesLimits_d)

N_dc, B_dc, A_dc, b_dc, c_dc, v_dc, origSize_dc, origVar_dc = parse_to_canon(A_d, b_d, c_d, v_d, limSigns_d, extrSign_d, valuesLimits_d)
print("-= DUAL CANON TASK =-")
print_task_as_canon(A_dc, b_dc, c_dc, v_dc)
print("solution:")
solution = convert_canon_solution_to_original(solve_brute_force(A_dc, b_dc, c_dc, v_dc), origSize_dc, origVar_dc)
print(solution)
print(np.dot(solution, c_d))
# МЕСТО ПОД РЕШЕНИЕ СИМПЛЕКСОМ
A_dc_std, b_dc_std, c_dc_std, v_dc_std, origSize_dc_std, origVar_dc_std = parse_to_standart(A_d, b_d, c_d, v_d, limSigns_d, extrSign_d, valuesLimits_d)
N_dc_s, B_dc_s, A_dc_s, b_dc_s, c_dc_s, v_dc_s = init_simplex(A_dc_std, b_dc_std, c_dc_std)
print(A_d)
print(c_d)
print("simplex solution:")
solution = convert_canon_solution_to_original(simplex(N_dc_s, B_dc_s, A_dc_s, b_dc_s, c_dc_s, v_dc_s), origSize_dc_std, origVar_dc_std)
print(solution)
print(np.dot(solution, c_d))
