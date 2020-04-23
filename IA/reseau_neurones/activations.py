import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivee(x):
    return sigmoid(x) * (1 - sigmoid(x))


def tanh(x):
    return np.tanh(x)


def tanh_derivee(x):
    return 1 - np.tanh(x) ** 2


def relu(x):
    return np.fmax(0, x)


def relu_derivee(x):
    x[x >= 0] = 1
    x[x < 0] = 0
    return x


def bent_identity(x):
    return (((x ** 2 + 1) ** 0.5 - 1) / 2) + x


def bent_identity_derivee(x):
    return (x / (2 * (x ** 2 + 1) ** 0.5)) + 1
