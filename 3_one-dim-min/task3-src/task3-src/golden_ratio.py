import math as m
import task as t

class GoldenRatioSolver:
    def __init__(self, task):
        self.task = task
        #self.GOLDEN_RATIO_CONST = 1.6180339887498948482045868343656381177203091798057628621
        self.GOLDEN_RATIO_CONST = (3 - m.sqrt(5)) / 2
        return

    def goldenRatioSolver(self, eps : float):
        lBorder = self.task.getLeftBorder()
        rBorder = self.task.getRightBorder()

        while abs(lBorder - rBorder) > eps:
            #x1 = rBorder - (rBorder - lBorder) / self.GOLDEN_RATIO_CONST
            #x2 = lBorder + (rBorder - lBorder) / self.GOLDEN_RATIO_CONST
            x1 = lBorder + self.GOLDEN_RATIO_CONST * (rBorder - lBorder)
            x2 = lBorder + (1 - self.GOLDEN_RATIO_CONST) * (rBorder - lBorder)

            y1 = self.task.f(x1)
            y2 = self.task.f(x2)

            if y1 >= y2:
                lBorder = x1
            else:
                rBorder = x2

        return (lBorder + rBorder) / 2
