from task_manager import read_task
#from standart_task_manager import parse_to_standart
from canon_task_manager import parse_to_canon, print_task_as_canon, convert_canon_solution_to_original
from dual_task_manager import parse_to_dual, print_task_as_dual
from brute_force import solve_brute_force
from simplex_solver import simplex
from simplex_solver import init_simplex

from cormen_canon_old_stuff import cormens_parse_to_canon

A, b, c, v, limSigns, extrSign, valuesLimits = read_task("task.txt")
#A_s, b_s, c_s, v_s, origSize_s, origVar_s = parse_to_standart(A, b, c, v, limSigns, extrSign, valuesLimits)

A_c, b_c, c_c, v_c, origSize_c, origVar_c = parse_to_canon(A, b, c, v, limSigns, extrSign, valuesLimits)
print("-= CANON TASK =-")
print_task_as_canon(A_c, b_c, c_c, v_c)
print("solution:")
print(convert_canon_solution_to_original(solve_brute_force(A_c, b_c, c_c, v_c), origSize_c, origVar_c))
# МЕСТО ПОД РЕШЕНИЕ СИМПЛЕКСОМ

A_cc, b_cc, c_cc, v_cc, oorigSize_cc, origVar_cc = cormens_parse_to_canon(A, b, c, v, limSigns, extrSign, valuesLimits)

N_s, B_s, A_s, b_s, c_s, v_s = init_simplex(A_cc, b_cc, c_cc)
print("simplex solution:")
print(convert_canon_solution_to_original(simplex(N_s, B_s, A_s, b_s, c_s, v_s), origSize_cc, origVar_cc))

A_d, b_d, c_d, v_d, limSigns_d, extrSign_d, valuesLimits_d = parse_to_dual(A, b, c, v, limSigns, extrSign, valuesLimits)
print("-= DUAL TASK =-")
print_task_as_dual(A_d, b_d, c_d, v_d, limSigns_d, extrSign_d, valuesLimits_d)

A_dc, b_dc, c_dc, v_dc, origSize_dc, origVar_dc = parse_to_canon(A_d, b_d, c_d, v_d, limSigns_d, extrSign_d, valuesLimits_d)
print("-= DUAL CANON TASK =-")
print_task_as_canon(A_dc, b_dc, c_dc, v_dc)
print("solution:")
print(convert_canon_solution_to_original(solve_brute_force(A_dc, b_dc, c_dc, v_dc), origSize_dc, origVar_dc))
# МЕСТО ПОД РЕШЕНИЕ СИМПЛЕКСОМ
