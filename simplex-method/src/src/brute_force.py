from itertools import combinations
import numpy as np

def get_basis_matrs(A : np.ndarray):
    N = A.shape[0]
    M = A.shape[1]

    basis_matrs = []
    basis_combinations_indexes = []
    all_indexes = [i for i in range(M)]

    for i in combinations(all_indexes, N):
        basis_matr = A[:, i]
        if np.linalg.det(basis_matr) != 0:
            basis_matrs.append(basis_matr)
            basis_combinations_indexes.append(i)

    return basis_matrs, basis_combinations_indexes

def get_all_possible_vectors(A : list, b : list):
    N = len(A[0])
    M = len(A)
    vectors = []

    if M >= N:
        return vectors
    else:
        basis_matrs, basis_combinations_indexes = get_basis_matrs(np.array(A))

    for i in range(len(basis_matrs)):
        solve = np.linalg.solve(basis_matrs[i], b)
        if (len(solve[solve < 0]) != 0) or (len(solve[solve > 1e+15]) != 0):
            continue

        vec = [0 for i in range(N)]
        for j in range(len(basis_combinations_indexes[i])):
            vec[basis_combinations_indexes[i][j]] = solve[j]
        vectors.append(vec)
    return vectors

#def solve_brute_force(A : list, b : list, c : list, v : float, targetSign : str):
def solve_brute_force(A : list, b : list, c : list, v : float):
    #if targetSign == "max":
    #    c_tmp = [coef * -1 for coef in c]
    #else:
    c_tmp = [coef for coef in c]

    vectors = get_all_possible_vectors(A, b)
    if len(vectors) == 0:
        return []

    solution = vectors[0]
    target_max = np.dot(solution, c_tmp)

    for vec in vectors:
        if np.dot(vec, c_tmp) > target_max:
            target_max = np.dot(vec, c_tmp)
            solution = vec

    return solution