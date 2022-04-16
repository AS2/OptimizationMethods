import numpy as np
from math import cos, sin, exp

class Task:
    def __init__(self):
        self.dimention = 2
        self.answer = [0.3, 0.5]    # actualy, not true -> need to find in net
        return

    # INITS BY USER
    def f(self, x : list) -> float:
        # RETURN VALUE OF FUNC
        x1 = x[0]
        x2 = x[1]
        return 2 * (x1 ** 2) + (x2 ** 2) + cos(x1 + x2) + 3 * x1 + 4 * x2
        #return (x1 ** 2) + 2*(x2 ** 2) + exp((x1 ** 2) + (x2 ** 2))

    # INITS BY USER
    def grad_f(self, x : list) -> list:
        # RETURN VEC OF DIFFS.
        x1 = x[0]
        x2 = x[1]

        df_1 = 4 * x1 - sin(x1 + x2) + 3
        df_2 = 2 * x2 - sin(x1 + x2) + 4
        #df_1 = 2 * x1 * (exp((x1 ** 2) + (x2 ** 2)) + 1)
        #df_2 = 2 * x2 * (exp((x1 ** 2) + (x2 ** 2)) + 2)
        return [df_1, df_2]

    # INITS BY USER
    def secGrad_f(self, x : list) -> list:
        # RETURN VEC OF DIFFS.
        x1 = x[0]
        x2 = x[1]

        df_11 = 4 - cos(x1 + x2)
        df_12 = -cos(x1 + x2)
        df_21 = -cos(x1 + x2)
        df_22 = 2 - cos(x1 + x2)
        return [[df_11, df_12], [df_21, df_22]]
