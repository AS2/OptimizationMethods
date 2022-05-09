from logging import exception
import numpy as np

ZERO_EPS = 0.00001

# some vec operations
def vecMul(a : float, x : list) -> list:
    return [a*xi for xi in x]

def vecSum(x : list, y : list) -> list:
    if len(x) != len(y):
        raise exception("Uncorrected vectors sizes")
    return [x[i] + y[i] for i in range(len(x))]

# useful funcs in Zoitendijk method
def getActiveIndexes(limits : list, x : list) -> list:
    indexes = list()

    for i in range(len(limits)):
        if abs(limits[i](x)) < ZERO_EPS:
            indexes.append(i)

    return indexes

def getPassiveIndexes(limits : list, x : list) -> list:
    indexes = list()

    for i in range(len(limits)):
        if limits[i](x) < 0:
            indexes.append(i)

    return indexes

def getNearActiveIndexes(limits : list, x : list, delta : float) -> list:
    indexes = list()

    for i in range(len(limits)):
        if limits[i](x) <= 0 and limits[i](x) >= -delta:
            indexes.append(i)

    return indexes
    