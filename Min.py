import numpy as np
from scipy.optimize import minimize


def f(x, y):
    return (x-1.23456789)**2


res = minimize(f, 0, method='BFGS', jac=False)

print(res.x)
