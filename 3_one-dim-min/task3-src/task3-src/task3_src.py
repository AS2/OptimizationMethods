import task as t
import golden_ratio as grm
import dichotomy_method as dm

EPS = [0.1, 0.01, 0.001]
currentTask = t.Task()
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