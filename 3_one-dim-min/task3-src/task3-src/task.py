import numpy as np
# FILE WITH TASK FORMULARIZATION
# TASK GRAPH https://www.desmos.com/calculator/isihbfhk1s

class Task:
    def __init__(self):
        self.a = 0.5
        self.b = 1
        self.delta = 0.05

        self.counter = 0
        self.truAnswer = 0.682212417467 # ans of alt task (from wolfram)
        return


    def f(self, x : float):
        someLittleEpsForX = 0.00001

        if (x < self.a - someLittleEpsForX) or (x > self.b + someLittleEpsForX):
            raise Exception("UNRESOLVED X")

        self.counter += 1

        # RETURN VALUE OF FUNC
        return 10 * (x - 0.3) * np.log(x - 0.3) - ((x - 0.3) ** 2) / 2
        #return 10 * x * np.log(x) - (x ** 2) / 2

    def printResult(self, potential_min : float, current_eps : float):
        someLittleEpsForX = 0.00001
        if (potential_min  < self.a - someLittleEpsForX) or (potential_min > self.b + someLittleEpsForX):
            raise Exception("UNRESOLVED X")

        count = self.counter
        print("Eps = " + str(current_eps))
        print("True is " + str(self.truAnswer))
        print("Potential answer is " + str(potential_min))
        print("Delta: " + str(abs(potential_min - self.truAnswer)))
        print("f(x) = " + str(self.f(potential_min)))
        print("Counter: " + str(count))
        return

    def restartCounter(self):
        self.counter = 0
        return

    def getLeftBorder(self):
        return self.a

    def getRightBorder(self):
        return self.b

    def getDelta(self):
        return self.delta
