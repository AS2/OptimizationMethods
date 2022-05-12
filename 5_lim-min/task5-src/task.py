from math import cos, sin

class Task:
    def __init__(self):
        self.dimention = 3
        self.answer = [0.3, 0.5, 0.7]    # actualy, not true -> need to find in net

        # limits with '<= 0' sign
        self.limits = [
            # sphere with Center (0, 0, 0) and Radius 4
            lambda x : x[0] ** 2 + x[1] ** 2 + x[2] ** 2 - 16,
            # cylinder with Center (0, 0, 0) and Radius 3
            lambda x : x[0] ** 2 + x[1] ** 2 - 9,
            # some more for 3rd coord, idk
            lambda x : x[0] ** 2  - (8),
        ]

        # gradients for limits with '<= 0' sign
        self.d_limits = [
            # sphere with Center (0, 0, 0) and Radius 3
            lambda x : [2 * x[0],
                        2 * x[1],
                        2 * x[2]], 
            # cylinder with Center (0, 0, 0) and Radius 2
            lambda x : [2 * x[0],
                        2 * x[1],
                        0],
            # some more for 3rd coord, idk
            lambda x : [2 * x[0],
                        0,
                        0]
        ]

        # limits with '= b' sign
        self.A = [[0, 0, 1]]
        self.b = [0] 
        return

    # INITS BY USER
    def f(self, x : list) -> float:
        # RETURN VALUE OF FUNC
        x1 = x[0]
        x2 = x[1]
        x3 = x[2]
        return 2 * (x1 ** 2) + (x2 ** 2) + 4 * (x3 ** 2) + cos(x1 + x2) + 3 * x1 + 4 * x2 + 8 * x3
        
    # INITS BY USER
    def grad_f(self, x : list) -> list:
        # RETURN VEC OF DIFFS.
        x1 = x[0]
        x2 = x[1]
        x3 = x[2]

        df_1 = 4 * x1 - sin(x1 + x2) + 3
        df_2 = 2 * x2 - sin(x1 + x2) + 4
        df_3 = 8 * x3 + 8
        return [df_1, df_2, df_3]
