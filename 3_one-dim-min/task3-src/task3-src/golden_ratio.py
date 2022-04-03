import math as m
import task as t

class GoldenRatioSolver:
    def __init__(self, task):
        self.task = task
        self.GOLDEN_RATIO_CONST = (1 + m.sqrt(5)) / 2
        return

    def goldenRatioSolver(self, eps : float):
        lBorder = self.task.getLeftBorder()
        rBorder = self.task.getRightBorder()

        x1 = rBorder - (rBorder - lBorder) / self.GOLDEN_RATIO_CONST
        x2 = lBorder + (rBorder - lBorder) / self.GOLDEN_RATIO_CONST
        y1 = self.task.f(x1)
        y2 = self.task.f(x2)

        while abs(lBorder - rBorder) > eps:
            if y1 <= y2:
                rBorder = x2
                x2 = x1
                y2 = y1

                x1 = rBorder - (rBorder - lBorder) / self.GOLDEN_RATIO_CONST
                y1 = self.task.f(x1)
            else:
                lBorder = x1
                x1 = x2
                y1 = y2

                x2 = lBorder + (rBorder - lBorder) / self.GOLDEN_RATIO_CONST
                y2 = self.task.f(x2)

        return (lBorder + rBorder) / 2
