from xmlrpc.client import boolean
import numpy as np
import math as m
import task as t
import utils as u

class GradWFragStep:
    def __init__(self, task : t.Task):
        self.task = task
        return

    # Function which will return first approximation of solution
    def firstApproxim(self, ) -> list:
        return

    # Function which will find additional direction
    def findDirection(self, x_k : list):
        return

    def ifZoitendijkMthodNeedToStop(self, selta_k : float) -> boolean:
        return

    # Function which will find minimum solving Zoitendijk method
    def zoutendijkSolver(self, delta : float, lambd : float, eps : float):
        # find first position
        x_min = self.firstApproxim()
        k = 0
        delta_k = delta

        while True:
            # Step 1: find additional direction

            # Step 2: find x_k and delta_k

            # if need to leave - leave)
            if self.ifZoitendijkMthodNeedToStop(delta_k):
                break

        return x_min
