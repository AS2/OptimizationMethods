import numpy as np
import math as m
import task as t
import utils as u
from scipy.optimize import linprog, OptimizeWarning
import warnings
from start_zoutendijk import SecZoutendijk as sz

warnings.simplefilter("error", OptimizeWarning)

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
            secZ = sz(self.task)
            x, eta = secZ.solver(1, 0.5)
            return x

    # Function which will find additional direction
    def findDirection(self, x_k : list, delta_k : float) -> list():
        nearActiveIndex = u.getNearActiveIndexes(self.task.limits, x_k, delta_k)

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
        activeLims = u.getActiveIndexes(self.task.limits, x_min)
        allRestrictionDeltas = list()
        for lim in range(len(self.task.limits)):
            if lim not in activeLims:
                allRestrictionDeltas.append(self.task.limits[lim](x_min))
        delta_0k = -max(allRestrictionDeltas)
        return (abs(eta_k) < u.ZERO_EPS and delta_k < delta_0k)

    def isNeedToFragmentStep(self, x_k : list, alpha_k : float, s_k : list, eta_k : float):
        x_tmp = u.vecSum(x_k, u.vecMul(alpha_k, s_k))
        firstCondition = self.task.f(x_tmp) <= self.task.f(x_k) + 1 / 2 * eta_k * alpha_k
        secondCondition = True

        for lim in self.task.limits:
            res = lim(x_tmp)
            secondCondition = secondCondition and (res <= 0)

        return (firstCondition and secondCondition) == False


    # Function which will find minimum solving Zoitendijk method
    def solver(self, alpha : float, lambd : float, x_0 : list):
        all_x = list()
        # find first position
        x_k = self.firstApproxim(x_0)
        all_x.append(x_k)

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
                all_x.append(x_k)
            else:
                delta_k = lambd * delta_k

            # if need to leave - leave)
            if self.ifZoitendijkMethodNeedToStop(x_k, delta_k, eta_k):
                break

        return all_x
