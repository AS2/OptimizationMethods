import matplotlib.pyplot as plt
import numpy as np

import task as t
import golden_ratio as grm
import dichotomy_method as dm

EPS = [0.1, 0.01, 0.001]
currentTask = t.Task()

x = np.arange(0.5, 1, 0.01)
y = [currentTask.f(i) for i in x]
plt.axis([0.5, 1, currentTask.f(currentTask.truAnswer) - 0.1, currentTask.f(1)])
plt.title('f(x) = 10 * (x - 0.3) * ln(x - 0.3) - (x - 0.3)^2 / 2')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.plot(x, y, 'r', currentTask.truAnswer, currentTask.f(currentTask.truAnswer), 'b*')
plt.grid(True)
plt.show()

grmSolver = grm.GoldenRatioSolver(currentTask)
dmSolver = dm.DichotomySolver(currentTask)
print("GRM SOLVE RESULTS:")
for eps in EPS:
    currentTask.restartCounter()
    currentTask.printResult(grmSolver.goldenRatioSolver(eps), eps)
    print()

print()
print("DM SOLVE RESULTS:")
for eps in EPS:
    currentTask.restartCounter()
    currentTask.printResult(dmSolver.dichotomySolver(eps), eps)
    print()
