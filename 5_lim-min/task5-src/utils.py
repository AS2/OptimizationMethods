from logging import exception
import numpy as np

def secNorm(x : list) -> float:
    return np.sum([xi ** 2 for xi in x])

def vecMul(a : float, x : list) -> list:
    return [a*xi for xi in x]

def vecSum(x : list, y : list) -> list:
    if len(x) != len(y):
        raise exception("Uncorrected vectors sizes")
    return [x[i] + y[i] for i in range(len(x))]
    