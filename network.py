import random
import numpy as np


class Network:
    def __init__(self, sizes):
        self.numLayers = len(sizes)
        self.sizes = sizes

        # bias is 2d array where each inner list
        # corresponds to every layer except the first with
        # length equal to how many nodes there are in each layer
        self.bias = [np.random.randn(layer, 1) for layer in sizes[1:]]

        # weight is a matrix of matrices where each inner matrix has
        # dimensions l2 by l1 so you can multiply by a vector
        # of length l1, which would be your previous layer
        self.weight = [np.random.randn(l2, l1)
                       for l1, l2 in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        for b, w in zip(self.bias, self.weight):
            a = sigmoid(np.dot(w, a) + b.flatten())
        return a

    def stochastic_gradient_descent(self, training_data, training_weight,
                                    epochs, eta):

        for epoch in range(epochs):
            # shuffle
            random.shuffle(training_data)

            # update each batch
            for mini_batch, tw in zip(training_data, training_weight):
                self.update_mini_batch(mini_batch, tw, eta)

            print("epoch {0}: complete".format(epoch))

    def update_mini_batch(self, mini_batch, end, eta):
        # initialize zero filled array of difference in biases and weights
        # back prop with values from batch
        # update bias and weight
        grad_bias = [np.zeros(b.shape) for b in self.bias]
        grad_weight = [np.zeros(w.shape) for w in self.weight]
        for x, y in mini_batch:
            delta_grad_bias, delta_grad_weight = self.backprop(x, y, end)
            grad_bias = np.array([gb.flatten() + dgb for gb, dgb in
                                  zip(grad_bias, delta_grad_bias)])
            grad_weight = np.array([gw + dgw for gw, dgw in
                                    zip(grad_weight, delta_grad_weight)])
        self.bias = [b.flatten() - (eta/(len(mini_batch)+1))*gb
                     for b, gb in zip(self.bias, grad_bias)]
        self.weight = [w - (eta / (len(mini_batch)+1)) * gw
                       for w, gw in zip(self.weight, grad_weight)]

    def backprop(self, x, y, end):
        grad_bias = [np.zeros(b.shape) for b in self.bias]
        grad_weight = [np.zeros(w.shape) for w in self.weight]

        # feedforward
        activation = x
        activations = [x] # storing activations layer by layer
        zs = [] # store all the z vectors layer by layer

        for b, w in zip(self.bias, self.weight):
            z = np.dot(w, activation) + b.flatten()
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)

        # actual backpropagation

        # our "cost gradient" here is a scalar, the end score, multiplied
        # by the difference between what we want and what is outputted
        # almost the same as normal except for the sum, which
        # reinforces better games while "discouraging" worse performance
        delta = end.sum() * (y - activations[-1])
        grad_bias[-1] = delta
        grad_weight[-1] = np.outer(delta, activations[-2])

        for layer in range(2, self.numLayers):

            delta = np.dot((self.weight[-layer+1]).transpose(), delta)
            grad_bias[-layer] = delta
            grad_weight[-layer] = np.outer(delta, activations[-layer-1])

        return grad_bias, grad_weight


# activation functions
def sigmoid(z, prime=False):
    if prime:
        sigmoid(z)(1-sigmoid(z))
    else:
        return 1 / (1 + np.exp(-z))


def tanh(z, prime=False):
    if prime:
        return 1 - np.square(tanh(z))
    else:
        return np.sinh(z)/np.cosh(z)