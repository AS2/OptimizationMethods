import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import math as m

import task as t
import gradWFragStep as gwfs
import gradBFGS as gbfgs

def taskPlot():
    x = np.arange(-4, 1, 0.05)
    y = np.arange(-4, 1, 0.05)
    xgrid, ygrid = np.meshgrid(x, y)
    zgrid = 2*(xgrid**2) + ygrid**2 + np.cos(xgrid + ygrid) + 3 * xgrid + 4 * ygrid

    fig = plt.figure(figsize=(7, 4))
    ax_3d = Axes3D(fig)

    #  Создаем массив RGB цветов каждой области:
    ax_3d.plot_surface(xgrid, ygrid, zgrid, rstride=5, cstride=5, cmap=cm.jet)
    plt.show()
    return

def printResult(steps : list, iters : int, fres : float, eps : float, methodName : str):
    print(methodName)
    print("Eps: " + str(eps))
    print("Res: " + str(steps[len(steps) - 1]))
    print("f(Res): " + str(fres))
    print("Iters: " + str(iters))
    return

def plotSteps(steps : list):
    xCoord = np.arange(-4, 1, 0.05)
    yCoord = np.arange(-4, 1, 0.05)
    x, y = np.meshgrid(xCoord, yCoord)
    z = 2*(x**2) + y**2 + np.cos(x + y) + 3 * x + 4 * y

    fig, ax = plt.subplots()

    fig.set_figwidth(8)     #  ширина и
    fig.set_figheight(8)    #  высота "Figure"

    xSteps = [step[0] for step in steps]
    ySteps = [step[1] for step in steps]
    #plt.title("Line levels of '")
    plt.plot(xSteps, ySteps, "bo--")
    cs = plt.contour(x, y, z)
    plt.clabel(cs)
    plt.show()
    return

def main():
    EPS = [0.00001]
    currentTask = t.Task()

    #taskPlot()
    gradWFragStep = gwfs.GradWFragStep(currentTask)
    grafBFGS = gbfgs.GrafBFGS(currentTask)

    for ep in EPS:
        steps, iters = gradWFragStep.gradWFragStepSolver(ep)
        printResult(steps, iters, currentTask.f(steps[len(steps) - 1]), ep, "GRADIENT WITH FRAG STEP")
        #if (ep == EPS[len(EPS) - 1]):
        #    plotSteps(steps)

    # Alghoritm - https://habr.com/ru/post/333356/
    for ep in EPS:
        steps, iters = grafBFGS.grafBFGSSolver(ep)
        printResult(steps, iters, currentTask.f(steps[len(steps) - 1]), ep, "BFGS METHOD")
        #if (ep == EPS[len(EPS) - 1]):
        #    plotSteps(steps)

    #steps, iters = gradWFragStep.gradWFragStepSolver(0.000001)
    #print(steps[len(steps) - 1])
    #print(m.sin(steps[len(steps) - 1][0] + steps[len(steps) - 1][1]))
    #print(currentTask.grad_f(steps[len(steps) - 1]))


main()
