import numpy as np
import numpy.linalg as ln
import scipy as sp
import scipy.optimize as opt

import task as t
import utils as u

class GrafBFGS:
    def __init__(self, task : t.Task):
        self.task = task
        return

    def findAlpha(self, xk, pk):
        a = 0.0000001
        b= 50
        eps = 0.000001

        while (abs(b - a) > eps):
            xm = (b + a) / 2
            delta = (b - a) / 100
            y1 = self.task.f(xk + (xm - delta) * pk)
            y2 = self.task.f(xk + (xm + delta) * pk)

            if (y1 > y2):
                a = xm
            else:
                b = xm

        return (b + a) / 2

    def grafBFGSSolver(self, eps : float):
        iter = 0
        k = 1
        xk = [0, 0]

        all_x = list()
        all_x.append(xk)

        d_f = self.task.grad_f(xk)

        # zero (start) init
        I = np.eye(len(xk), dtype=float)
        Ak = I

        while ln.norm(d_f) > eps:
            pk = -np.dot(Ak, d_f)

            # ищем линейным поиском (но можно и просто а = 1)
            alpha_k = self.findAlpha(xk, pk)
            #line_search = opt.line_search(self.task.f, self.task.grad_f, xk, pk)
            #if len(line_search) > 0 and line_search[0] != None:
            #    alpha_k = line_search[0]
            #else:
            #    alpha_k = 0.005
            
            xk_p1 = u.vecSum(xk, u.vecMul(alpha_k, pk))
            sk = u.vecSum(xk_p1, u.vecMul(-1, xk))
            xk = xk_p1
            all_x.append(xk)

            d_f_p1 = self.task.grad_f(xk_p1)
            yk = u.vecSum(d_f_p1, u.vecMul(-1, d_f))
            d_f = d_f_p1
        
            if (k % 10 == 0):
                Ak = I
                k = 1
            else:
                ro = 1.0 / (np.dot(yk, sk))

                sk = np.array(sk)
                yk = np.array(yk)
                sk = sk.reshape(-1, 1)
                yk = yk.reshape(-1, 1)

                
                m1 = ro * np.matmul(sk, np.transpose(yk))
                m2 = ro * np.matmul(yk, np.transpose(sk))
                A1 = I - m1
                A2 = I - m2
                A3 = ro * np.matmul(sk, np.transpose(sk))
                Ak = np.matmul(A1, np.matmul(Ak, A2)) + A3
                k += 1
            iter += 1
        
        return all_x, iter