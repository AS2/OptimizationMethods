import task as t

class DichotomySolver:
    def __init__(self, task : t.Task):
        self.task = task
        return

    def dichotomySolver(self, eps : float):
        lBorder = self.task.getLeftBorder()
        rBorder = self.task.getRightBorder()

        while abs(lBorder - rBorder) > eps:
            m = (lBorder + rBorder) / 2
            delta = self.task.getDelta() * (lBorder - rBorder)
            y1 = self.task.f(m - delta)
            y2 = self.task.f(m + delta)

            if y1 >= y2:
                lBorder = m
            else:
                rBorder = m

        return (lBorder + rBorder) / 2
