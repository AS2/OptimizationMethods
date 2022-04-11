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

    def grafBFGSSolver(self, eps : float):
        iter = 0
        x_tmp = [0, 0]
        all_x = list()
        all_x.append(x_tmp)

        d_f = self.task.grad_f(x_tmp)

        # zero (start) init
        I = np.eye(len(x_tmp), dtype=int)
        xk = x_tmp
        Hk = I
   
        while ln.norm(d_f) > eps:
    
            pk = -np.dot(Hk, d_f)

            # ищем линейным поиском (но можно и просто а = 1)
            line_search = opt.line_search(self.task.f, self.task.grad_f, xk, pk)
            alpha_k = line_search[0]
            #alpha_k = 1
        
            xk_p1 = u.vecSum(xk, u.vecMul(alpha_k, pk))
            sk = u.vecSum(xk_p1, u.vecMul(-1, xk))
            xk = xk_p1
            all_x.append(xk)
        
            d_f_p1 = self.task.grad_f(xk_p1)
            yk = u.vecSum(d_f_p1, u.vecMul(-1, d_f))
            d_f = d_f_p1
        
            iter += 1
        
            ro = 1.0 / (np.dot(yk, sk))
            A1 = I - ro * np.matmul(sk, np.transpose(yk))
            A2 = I - ro * np.matmul(yk, np.transpose(sk))
            Hk = np.dot(A1, np.dot(Hk, A2)) + (ro * np.matmul(sk, np.transpose(sk)))
        
        return all_x, iter