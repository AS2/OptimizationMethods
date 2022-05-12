import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import math as m

import task as t
import zoutendijk as z

def taskPlot():
    x = np.arange(-4, 4, 0.05)
    y = np.arange(-4, 4, 0.05)
    xgrid, ygrid = np.meshgrid(x, y)
    zgrid = 2*(xgrid**2) + ygrid**2 + np.cos(xgrid + ygrid) + 3 * xgrid + 4 * ygrid

    fig = plt.figure(figsize=(7, 4))
    ax_3d = Axes3D(fig)

    #  Создаем массив RGB цветов каждой области:
    ax_3d.plot_surface(xgrid, ygrid, zgrid, rstride=5, cstride=5, cmap=cm.jet)
    plt.show()
    return

def printResult(steps : list, f_min : float):
    iters = len(steps) - 1
    print("-= MAIN RESULT =-")
    print("iters: " + str(iters))
    print("x_min: " + str(steps[len(steps) - 1]))
    print("f(x_min) = " + str(f_min))
    
    print("-= EACH STEP RESULT =-")
    for i in range(len(steps)):
        if (i == 0):
            print("first approximation: " + str(steps[i]))
        else:
            print("iter #" + str(i) + ". x_" + str(i) + ": " + str(steps[i]))
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
    xRest    =  np.arange(-4, 1, 0.002)
    yRest1_1 =  np.sqrt(16 - xRest ** 2)
    yRest1_2 = -np.sqrt(16 - xRest ** 2)
    yRest2_1 =  np.sqrt(9 - xRest ** 2)
    yRest2_2 = -np.sqrt(9 - xRest ** 2)
    yRest    =  np.arange(-4, 1, 0.002)
    xRest3_2 = -np.sqrt(8) + yRest - yRest
    #plt.title("Line levels of '")
    plt.xlim([-4, 1])
    plt.ylim([-4, 1])
    plt.plot(xSteps, ySteps, "bo--")
    # rest 1
    plt.plot(xRest, yRest1_1, "r-")
    plt.plot(xRest, yRest1_2, "r-")
    # rest 2
    plt.plot(xRest, yRest2_1, "y-")
    plt.plot(xRest, yRest2_2, "y-")
    # rest 3
    plt.plot(xRest3_2, yRest, "k-")
    cs = plt.contour(x, y, z)
    plt.clabel(cs)
    plt.show()
    return

def plotS(steps : list):
    xCoord = np.arange(-4, 4, 0.05)
    yCoord = np.arange(-4, 4, 0.05)
    x, y = np.meshgrid(xCoord, yCoord)
    z = 2*(x**2) + y**2 + np.cos(x + y) + 3 * x + 4 * y

    fig, ax = plt.subplots()

    fig.set_figwidth(8)     #  ширина и
    fig.set_figheight(8)    #  высота "Figure"

    xSteps = [step[0] for step in steps]
    ySteps = [step[1] for step in steps]
    xRest    =  np.arange(-4, 4 + 0.002, 0.002)
    yRest1_1 =  np.sqrt(16 - xRest ** 2)
    yRest1_2 = -np.sqrt(16 - xRest ** 2)
    yRest2_1 =  np.sqrt(9 - xRest ** 2)
    yRest2_2 = -np.sqrt(9 - xRest ** 2)
    yRest    =  np.arange(-4, 4 + 0.002, 0.002)
    xRest3_1 =  0.805673 + yRest - yRest
    xRest3_2 =  -0.805673 + yRest - yRest
    #plt.title("Line levels of '")
    plt.xlim([-4, 4])
    plt.ylim([-4, 4])
    plt.plot(xSteps[len(xSteps) - 1], ySteps[len(xSteps) - 1], "k*--")
    # rest 1
    plt.plot(xRest, yRest1_1, "r-")
    plt.plot(xRest, yRest1_2, "r-")
    # rest 2
    plt.plot(xRest, yRest2_1, "y-")
    plt.plot(xRest, yRest2_2, "y-")
    # rest 3
    plt.plot(xRest3_1, yRest, "k-")
    plt.plot(xRest3_2, yRest, "k-")
    cs = plt.contour(x, y, z)
    plt.clabel(cs)
    plt.show()
    return

def main():
    #taskPlot()
    currentTask = t.Task()

    zoitendijkSolver = z.Zoitendijk(currentTask)

    steps = zoitendijkSolver.solver(1, 0.5, [10.0, 10.0, 10.0])
    printResult(steps, currentTask.f(steps[len(steps) - 1]))
    #plotSteps(steps)
    #plotS(steps)
    return
main()
