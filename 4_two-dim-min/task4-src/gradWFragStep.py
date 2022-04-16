import numpy as np
import math as m
import task as t
import utils as u

class GradWFragStep:
    def __init__(self, task : t.Task):
        self.task = task
        return

    def gradWFragStepSolver(self, eps : float):
        x_tmp = [0, 0]
        alpha_zero = 0.5
        lambd = 0.6
        delta = 0.5

        iters = 0
        all_x = list()
        all_x.append(x_tmp)

        grad_f = self.task.grad_f(x_tmp)
        while m.sqrt(u.secNorm(grad_f)) > eps:
            ak = alpha_zero
            f = self.task.f(u.vecSum(x_tmp, u.vecMul(-ak, grad_f)))
            fk = self.task.f(x_tmp)
            
            while (f - fk >= -delta * ak * u.secNorm(grad_f)):
                ak = lambd * ak
                f = self.task.f(u.vecSum(x_tmp, u.vecMul(-ak, grad_f)))
                fk = self.task.f(x_tmp)

            x_tmp = u.vecSum(x_tmp, u.vecMul(-ak, grad_f))
            grad_f = self.task.grad_f(x_tmp)
            all_x.append(x_tmp)
            iters += 1

        return all_x, iters
