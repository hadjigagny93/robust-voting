""" Optimizers class """
from scipy.optimize import minimize
import numpy as np
import math


class Optimizer:
    def __init__(self, tolerance=1e-6, max_iter=100):
        self.tolerance = tolerance
        self.max_iter = max_iter

    def minimize(self, function, bounds):
        raise NotImplementedError


class ShelfOptimizer(Optimizer):
    def __init__(self, tolerance=1e-6, max_iter=100):
        super().__init__(tolerance=tolerance, max_iter=max_iter)

    def minimize(self, function, bounds):
        minimum_obj = minimize(function, np.array([0]*len(bounds)), bounds=bounds, tol=self.tolerance,
                              options={"maxiter": self.max_iter, "disp": False})

        return minimum_obj.x


def derivate(x, weights, values, delta=1, voting_resilience=1):
    """ computes the derivative of QrMed """
    deriv = voting_resilience * x
    for value, weight in zip(values, weights):
        if x <= value:
            deriv += weight * (math.exp((x - value)/delta) - 1)
        else:
            deriv += weight * (1 - math.exp((value - x)/delta))
    return deriv


def dichotomy(weights, values, delta=1, voting_resilience=1, nb_iter=100, bnds=(-10, 10)):
    inf, sup = bnds
    mid = (inf + sup) / 2
    for iter in range(nb_iter):
        if derivate(mid, weights, values, delta, voting_resilience) > 0:
            sup = mid
        else:
            inf = mid
        mid = (inf + sup) / 2
    return mid