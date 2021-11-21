from math import log, e
import numpy as np


def Uniform_Var():
    return np.random.uniform(0, 1)

def UniformAB_Var(a,b):
    u=np.random.uniform(0, 1)
    return a + (b-a)*u


def Exponential_Var(_lambda):
    u = Uniform_Var()
    return (-1/_lambda)*np.log(u)




