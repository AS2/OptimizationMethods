import numpy as np
import math as m
import task as t
import utils as u
from scipy.optimize import linprog, OptimizeWarning
import warnings

warnings.simplefilter("error", OptimizeWarning)
ZERO_EPS = 0.000001

class Zoitendijk:
    def __init__(self, task : t.Task):
        self.task = task
        return

    # Function which will return first approximation of solution
    def firstApproxim(self, x : list) -> list:
        eta = max([lim(x) for lim in self.task.limits])
        if (eta <= 0):
            return x
        else:
            valid = False
            while not valid:
                delta = -eta
                res = self.findDirection(x, delta)
                s = list()
                s, eta = res.x[0:(self.task.dimention - 1)], res.fun
                alpha = 1
                valid = False

                while not valid:
                    valid = not self.isNeedToFragmentStep(x, alpha, s, eta)
                    if not valid:
                        alpha *= 0.5
                        if (alpha < ZERO_EPS * ZERO_EPS):
                            alpha = 0.5
                            break
            x = u.vecSum(x, u.vecMul(alpha, s))
            return x

    # Function which will find additional direction
    def findDirection(self, x_k : list, delta_k : float) -> list():
        nearActiveIndex = self.task.getNearActiveIndexes(x_k, delta_k)

        A_ub = np.zeros(shape=(1 + len(nearActiveIndex), self.task.dimention + 1))
        b_ub = np.zeros(shape=(1 + len(nearActiveIndex), 1))
        for i in range(len(nearActiveIndex) + 1):
            if i == 0:
                grad = self.task.grad_f(x_k)
            else:
                index = nearActiveIndex[i - 1]
                grad = self.task.d_limits[index](x_k)
            for j in range(len(grad)):
                A_ub[i, j] = grad[j]
            A_ub[i, len(grad)] = -1


        A_eq = np.zeros(shape=(len(self.task.A), self.task.dimention + 1))
        b_eq = np.zeros(len(self.task.A))
        for i in range(len(self.task.A)):
            for j in range(len(self.task.A[i])):
                A_eq[i, j] = self.task.A[i][j]

        c = np.zeros(self.task.dimention + 1)
        c[self.task.dimention] = 1

        bounds = list()
        for i in range(self.task.dimention):
            bounds.append([-1, 1])
        bounds.append([None, None])

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return linprog(c, A_ub, b_ub, A_eq, b_eq, bounds, 'simplex')

    def ifZoitendijkMethodNeedToStop(self, x_min : list, delta_k : float, eta_k : float) -> bool:
        #activeLims = self.task.getActiveIndexes(x_min)
        #if len(activeLims) != 0:
        #    delta_0k = -max([self.task.limits[lim](x_min) for lim in activeLims])
        #else:
        #    delta_0k = delta_k + 1
        delta_0k = -max([lim(x_min) for lim in self.task.limits])

        return (abs(eta_k) < ZERO_EPS and delta_k < delta_0k)

    def isNeedToFragmentStep(self, x_k : list, alpha_k : float, s_k : list, eta_k : float):
        x_tmp = u.vecSum(x_k, u.vecMul(alpha_k, s_k))
        firstCondition = self.task.f(x_tmp) <= self.task.f(x_k) + 1 / 2 * eta_k * alpha_k
        secondCondition = True

        for lim in self.task.limits:
            secondCondition = secondCondition and (lim(x_tmp) <= ZERO_EPS)

        return (firstCondition and secondCondition) == False


    # Function which will find minimum solving Zoitendijk method
    def solver(self, alpha : float, lambd : float, x_0 : list):
        # find first position
        x_k = self.firstApproxim(x_0)
        k = 0
        alpha_k = alpha
        delta_k = 0.5

        while True:
            # Step 1: find additional direction
            s_and_eta = self.findDirection(x_k, delta_k)
            s_k = list()
            for i in range(len(s_and_eta.x) - 1):
                s_k.append(s_and_eta.x[i])
            eta_k = s_and_eta.x[len(s_and_eta.x) - 1]

            # Step 2: find x_k and delta_k
            if eta_k < -delta_k:
                alpha_k = alpha
                while self.isNeedToFragmentStep(x_k, alpha_k, s_k, eta_k):
                    alpha_k *= lambd
                x_k = u.vecSum(x_k, u.vecMul(alpha_k, s_k))
            else:
                delta_k = lambd * delta_k

            # if need to leave - leave)
            if self.ifZoitendijkMethodNeedToStop(x_k, delta_k, eta_k):
                break
            k += 1

        return x_k
