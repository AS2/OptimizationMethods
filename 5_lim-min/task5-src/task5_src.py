import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import math as m

import task as t
import zoutendijk as z

def printResult(x_min : list, f_min : float):
    print("x_min: " + str(x_min))
    print("f(x_min) = " + str(f_min))
    return

def main():
    currentTask = t.Task()

    zoitendijkSolver = z.Zoitendijk(currentTask)

    solution = zoitendijkSolver.solver(1, 0.5, [0.0, 0.0, 0.0])
    printResult(solution, currentTask.f(solution))

main()
