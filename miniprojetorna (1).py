# -*- coding: utf-8 -*-
"""MiniProjetoRNA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y9YLC5W3MnwavUD6Ki4j2z55p2K-KngT

Parte 1 - código inicial
"""

import numpy as np
from tensorflow.keras.datasets import mnist

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return np.where(x > 0, 1, 0)

def softmax(x):
    exps = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exps / np.sum(exps, axis=1, keepdims=True)

def cross_entropy_loss(y_true, y_pred):
    epsilon = 1e-8
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred))

class MLP:
    def __init__(self, input_size, hidden_size, output_size, learning_rate):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate

        self.weights1 = np.random.randn(self.input_size, self.hidden_size) * np.sqrt(2 / self.input_size)
        self.weights2 = np.random.randn(self.hidden_size, self.output_size) * np.sqrt(2 / self.hidden_size)

        self.bias1 = np.zeros((1, self.hidden_size))
        self.bias2 = np.zeros((1, self.output_size))

    def train(self, X, y, epochs, batch_size):
        num_examples = X.shape[0]
        iterations_per_epoch = num_examples // batch_size

        for epoch in range(epochs):
            for _ in range(iterations_per_epoch):
                indices = np.random.choice(num_examples, size=batch_size, replace=False)
                X_batch = X[indices]
                y_batch = y[indices]

                hidden_layer = relu(np.dot(X_batch, self.weights1) + self.bias1)
                output_layer = softmax(np.dot(hidden_layer, self.weights2) + self.bias2)

                output_error = y_batch - output_layer
                output_delta = output_error / batch_size

                hidden_error = output_delta.dot(self.weights2.T)
                hidden_delta = hidden_error * relu_derivative(hidden_layer)

                self.weights2 += hidden_layer.T.dot(output_delta) * self.learning_rate
                self.weights1 += X_batch.T.dot(hidden_delta) * self.learning_rate

                self.bias2 += np.sum(output_delta, axis=0) * self.learning_rate
                self.bias1 += np.sum(hidden_delta, axis=0) * self.learning_rate

    def predict(self, X):
        hidden_layer = relu(np.dot(X, self.weights1) + self.bias1)
        output_layer = softmax(np.dot(hidden_layer, self.weights2) + self.bias2)
        return np.argmax(output_layer, axis=1)

# Carregamento e pré-processamento dos dados MNIST
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(-1, 784) / 255.0
X_test = X_test.reshape(-1, 784) / 255.0

y_train_encoded = np.zeros((y_train.shape[0], 10))
y_train_encoded[np.arange(y_train.shape[0]), y_train] = 1

# Definição e treinamento da MLP
mlp = MLP(input_size=784, hidden_size=20, output_size=10, learning_rate=0.01)
mlp.train(X_train, y_train_encoded, epochs=500, batch_size=128)

# Avaliação da MLP
y_pred = mlp.predict(X_test)
accuracy = np.mean(y_pred == y_test)
print("Acurácia: {:.2%}".format(accuracy))

"""*Parte* 2 - Propagação para frente e custo total"""

import numpy as np
from tensorflow.keras.datasets import mnist

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return np.where(x > 0, 1, 0)

def softmax(x):
    exps = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exps / np.sum(exps, axis=1, keepdims=True)

def cross_entropy_loss(y_true, y_pred):
    epsilon = 1e-8
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred))

class MLP:
    def __init__(self, input_size, hidden_size, output_size, learning_rate):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate

        self.weights1 = np.random.randn(self.input_size, self.hidden_size) * np.sqrt(2 / self.input_size)
        self.weights2 = np.random.randn(self.hidden_size, self.output_size) * np.sqrt(2 / self.hidden_size)

        self.bias1 = np.zeros((1, self.hidden_size))
        self.bias2 = np.zeros((1, self.output_size))

    def forward_propagation(self, X):
        hidden_layer = relu(np.dot(X, self.weights1) + self.bias1)
        output_layer = softmax(np.dot(hidden_layer, self.weights2) + self.bias2)
        return hidden_layer, output_layer

    def train(self, X, y, epochs, batch_size):
        num_examples = X.shape[0]
        iterations_per_epoch = num_examples // batch_size

        for epoch in range(epochs):
            for _ in range(iterations_per_epoch):
                indices = np.random.choice(num_examples, size=batch_size, replace=False)
                X_batch = X[indices]
                y_batch = y[indices]

                hidden_layer, output_layer = self.forward_propagation(X_batch)

                output_error = y_batch - output_layer
                output_delta = output_error / batch_size

                hidden_error = output_delta.dot(self.weights2.T)
                hidden_delta = hidden_error * relu_derivative(hidden_layer)

                self.weights2 += hidden_layer.T.dot(output_delta) * self.learning_rate
                self.weights1 += X_batch.T.dot(hidden_delta) * self.learning_rate

                self.bias2 += np.sum(output_delta, axis=0) * self.learning_rate
                self.bias1 += np.sum(hidden_delta, axis=0) * self.learning_rate

            _, output = self.forward_propagation(X)
            cost = cross_entropy_loss(y, output)
            print(f"Epoch {epoch+1}/{epochs}, Cost: {cost}")

        total_cost = cross_entropy_loss(y, output)
        print(f"Total Cost: {total_cost}")

    def predict(self, X):
        _, output = self.forward_propagation(X)
        return np.argmax(output, axis=1)

# Loading and preprocessing the MNIST dataset
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(-1, 784) / 255.0
X_test = X_test.reshape(-1, 784) / 255.0

y_train_encoded = np.zeros((y_train.shape[0], 10))
y_train_encoded[np.arange(y_train.shape[0]), y_train] = 1

# Definição e treinamento da MLP
mlp = MLP(input_size=784, hidden_size=20, output_size=10, learning_rate=0.1)
mlp.train(X_train, y_train_encoded, epochs=200, batch_size=256)

# Avaliação da MLP
y_pred = mlp.predict(X_test)
accuracy = np.mean(y_pred == y_test)
print("Acurácia: {:.2%}".format(accuracy))

"""Parte 3 - Gradiente da função de custo"""

import numpy as np
from tensorflow.keras.datasets import mnist

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return np.where(x > 0, 1, 0)

def softmax(x):
    exps = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exps / np.sum(exps, axis=1, keepdims=True)

def cross_entropy_loss(y_true, y_pred):
    epsilon = 1e-8
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred))

class MLP:
    def __init__(self, input_size, hidden_sizes, output_size, learning_rate):
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        self.learning_rate = learning_rate

        self.weights = []
        self.biases = []
        self.num_layers = len(hidden_sizes) + 1

        sizes = [input_size] + hidden_sizes + [output_size]

        for i in range(1, self.num_layers + 1):
            self.weights.append(np.random.randn(sizes[i - 1], sizes[i]) * np.sqrt(2 / sizes[i - 1]))
            self.biases.append(np.zeros((1, sizes[i])))

    def forward_propagation(self, X):
        activations = [X]
        for i in range(self.num_layers):
            hidden_layer = relu(np.dot(activations[i], self.weights[i]) + self.biases[i])
            activations.append(hidden_layer)
        output_layer = softmax(np.dot(activations[-2], self.weights[-1]) + self.biases[-1])
        return activations, output_layer

    def train(self, X, y, epochs, batch_size):
        num_examples = X.shape[0]
        iterations_per_epoch = num_examples // batch_size

        for epoch in range(epochs):
            for _ in range(iterations_per_epoch):
                indices = np.random.choice(num_examples, size=batch_size, replace=False)
                X_batch = X[indices]
                y_batch = y[indices]

                activations, output_layer = self.forward_propagation(X_batch)

                output_error = y_batch - output_layer
                output_delta = output_error / batch_size

                deltas = [output_delta]

                for i in range(self.num_layers - 1, 0, -1):
                    hidden_error = deltas[-1].dot(self.weights[i].T)
                    hidden_delta = hidden_error * relu_derivative(activations[i])
                    deltas.append(hidden_delta)

                for i in range(self.num_layers - 1, -1, -1):
                    self.weights[i] += activations[i].T.dot(deltas[self.num_layers - 1 - i]) * self.learning_rate
                    self.biases[i] += np.sum(deltas[self.num_layers - 1 - i], axis=0) * self.learning_rate

            _, output = self.forward_propagation(X)
            cost = cross_entropy_loss(y, output)
            

        total_cost = cross_entropy_loss(y, output)
        

    def predict(self, X):
        _, output = self.forward_propagation(X)
        return np.argmax(output, axis=1)

    def calcular_gradiente(self, X, y):
        activations, output_layer = self.forward_propagation(X)
        output_error = y - output_layer
        output_delta = output_error / X.shape[0]

        deltas = [output_delta]

        for i in range(self.num_layers - 1, 0, -1):
            hidden_error = deltas[-1].dot(self.weights[i].T)
            hidden_delta = hidden_error * relu_derivative(activations[i])
            deltas.append(hidden_delta)

        gradients = []
        for i in range(self.num_layers - 1, -1, -1):
            weight_gradient = activations[i].T.dot(deltas[self.num_layers - 1 - i])
            bias_gradient = np.sum(deltas[self.num_layers - 1 - i], axis=0)
            gradients.append((weight_gradient, bias_gradient))

        return gradients


# Carregando e pré-processando o conjunto de dados MNIST
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(-1, 784) / 255.0
X_test = X_test.reshape(-1, 784) / 255.0

y_train_encoded = np.zeros((y_train.shape[0], 10))
y_train_encoded[np.arange(y_train.shape[0]), y_train] = 1

# Definição e treinamento da MLP com ajustes
mlp = MLP(input_size=784, hidden_sizes=[20, 20, 20], output_size=10, learning_rate=0.01)
mlp.train(X_train, y_train_encoded, epochs=450, batch_size=550)

# Calcular o gradiente da função custo
gradients = mlp.calcular_gradiente(X_train, y_train_encoded)

# Acessar os gradientes para cada camada
for i, (weight_gradient, bias_gradient) in enumerate(gradients):
    print(f"Gradiente para a camada {i + 1}:")
    print("Peso:")
    print(weight_gradient)
    print("Viés:")
    print(bias_gradient)
    print()

# Avaliação da MLP
y_pred = mlp.predict(X_test)
acuracia = np.mean(y_pred == y_test)
print("Acurácia: {:.2%}".format(acuracia))

"""PARTE 4 - Retropropagação"""

import numpy as np
from tensorflow.keras.datasets import mnist

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return np.where(x > 0, 1, 0)

def softmax(x):
    exps = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exps / np.sum(exps, axis=1, keepdims=True)

def cross_entropy_loss(y_true, y_pred):
    epsilon = 1e-8
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred))

class MLP:
    def __init__(self, input_size, hidden_sizes, output_size, learning_rate):
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        self.learning_rate = learning_rate

        self.weights1 = np.random.randn(self.input_size, self.hidden_sizes[0]) * np.sqrt(2 / self.input_size)
        self.weights2 = np.random.randn(self.hidden_sizes[0], self.hidden_sizes[1]) * np.sqrt(2 / self.hidden_sizes[0])
        self.weights3 = np.random.randn(self.hidden_sizes[1], self.output_size) * np.sqrt(2 / self.hidden_sizes[1])

        self.biases1 = np.zeros((1, self.hidden_sizes[0]))
        self.biases2 = np.zeros((1, self.hidden_sizes[1]))
        self.biases3 = np.zeros((1, self.output_size))

    def forward_propagation(self, X):
        hidden_layer1 = relu(np.dot(X, self.weights1) + self.biases1)
        hidden_layer2 = relu(np.dot(hidden_layer1, self.weights2) + self.biases2)
        output_layer = softmax(np.dot(hidden_layer2, self.weights3) + self.biases3)
        return hidden_layer1, hidden_layer2, output_layer

    def backward_propagation(self, X, y, hidden_layer1, hidden_layer2, output_layer):
        batch_size = X.shape[0]

        output_error = output_layer - y
        output_delta = output_error / batch_size

        hidden_error2 = output_delta.dot(self.weights3.T)
        hidden_delta2 = hidden_error2 * relu_derivative(hidden_layer2)

        hidden_error1 = hidden_delta2.dot(self.weights2.T)
        hidden_delta1 = hidden_error1 * relu_derivative(hidden_layer1)

        self.weights3 -= hidden_layer2.T.dot(output_delta) * self.learning_rate
        self.weights2 -= hidden_layer1.T.dot(hidden_delta2) * self.learning_rate
        self.weights1 -= X.T.dot(hidden_delta1) * self.learning_rate

        self.biases3 -= np.sum(output_delta, axis=0) * self.learning_rate
        self.biases2 -= np.sum(hidden_delta2, axis=0) * self.learning_rate
        self.biases1 -= np.sum(hidden_delta1, axis=0) * self.learning_rate

    def train(self, X, y, epochs, batch_size):
        num_examples = X.shape[0]
        iterations_per_epoch = num_examples // batch_size

        for epoch in range(epochs):
            for _ in range(iterations_per_epoch):
                indices = np.random.choice(num_examples, size=batch_size, replace=False)
                X_batch = X[indices]
                y_batch = y[indices]

                hidden_layer1, hidden_layer2, output_layer = self.forward_propagation(X_batch)

                self.backward_propagation(X_batch, y_batch, hidden_layer1, hidden_layer2, output_layer)

            _, _, output = self.forward_propagation(X)
            cost = cross_entropy_loss(y, output)

            

    def predict(self, X):
        _, _, output = self.forward_propagation(X)
        return np.argmax(output, axis=1)

# Loading and preprocessing the MNIST dataset
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(-1, 784) / 255.0
X_test = X_test.reshape(-1, 784) / 255.0

y_train_encoded = np.zeros((y_train.shape[0], 10))
y_train_encoded[np.arange(y_train.shape[0]), y_train] = 1

# Definition and training of the MLP
mlp = MLP(input_size=784, hidden_sizes=[20, 20], output_size=10, learning_rate=0.01)
mlp.train(X_train, y_train_encoded, epochs=500, batch_size=200)

# Evaluation of the MLP
y_pred = mlp.predict(X_test)
accuracy = np.mean(y_pred == y_test)
print("Accuracy: {:.2%}".format(accuracy))

"""Parte 5"""

import numpy as np
from tensorflow.keras.datasets import mnist

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return np.where(x > 0, 1, 0)

def softmax(x):
    exps = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exps / np.sum(exps, axis=1, keepdims=True)

def cross_entropy_loss(y_true, y_pred):
    epsilon = 1e-8
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred))

class MLP:
    def __init__(self, input_size, hidden_sizes, output_size, learning_rate):
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        self.learning_rate = learning_rate

        self.weights = []
        self.biases = []

        # Inicialização dos pesos e bias das camadas ocultas
        for i in range(len(hidden_sizes)):
            if i == 0:
                self.weights.append(np.random.randn(self.input_size, self.hidden_sizes[0]) * np.sqrt(2 / self.input_size))
                self.biases.append(np.zeros((1, self.hidden_sizes[0])))
            else:
                self.weights.append(np.random.randn(self.hidden_sizes[i-1], self.hidden_sizes[i]) * np.sqrt(2 / self.hidden_sizes[i-1]))
                self.biases.append(np.zeros((1, self.hidden_sizes[i])))

        # Inicialização dos pesos e bias da camada de saída
        self.weights.append(np.random.randn(self.hidden_sizes[-1], self.output_size) * np.sqrt(2 / self.hidden_sizes[-1]))
        self.biases.append(np.zeros((1, self.output_size)))

    def forward_propagation(self, X):
        hidden_layers = [relu(np.dot(X, self.weights[0]) + self.biases[0])]
        
        for i in range(1, len(self.hidden_sizes)):
            hidden_layers.append(relu(np.dot(hidden_layers[i-1], self.weights[i]) + self.biases[i]))
        
        output_layer = softmax(np.dot(hidden_layers[-1], self.weights[-1]) + self.biases[-1])
        return hidden_layers, output_layer

    def backward_propagation(self, X, y, hidden_layers, output_layer):
        batch_size = X.shape[0]

        output_error = output_layer - y
        output_delta = output_error / batch_size

        hidden_error = []
        hidden_delta = []

        hidden_error.append(output_delta.dot(self.weights[-1].T))
        hidden_delta.append(hidden_error[0] * relu_derivative(hidden_layers[-1]))

        for i in range(len(self.hidden_sizes) - 2, -1, -1):
            hidden_error.insert(0, hidden_delta[0].dot(self.weights[i+1].T))
            hidden_delta.insert(0, hidden_error[0] * relu_derivative(hidden_layers[i]))

        for i in range(len(self.hidden_sizes)):
            if i == 0:
                self.weights[i] -= X.T.dot(hidden_delta[i]) * self.learning_rate
            else:
                self.weights[i] -= hidden_layers[i-1].T.dot(hidden_delta[i]) * self.learning_rate
        
        self.weights[-1] -= hidden_layers[-1].T.dot(output_delta) * self.learning_rate

        for i in range(len(self.hidden_sizes)):
            self.biases[i] -= np.sum(hidden_delta[i], axis=0) * self.learning_rate
        
        self.biases[-1] -= np.sum(output_delta, axis=0) * self.learning_rate

    def train(self, X, y, epochs, batch_size):
        num_examples = X.shape[0]
        iterations_per_epoch = num_examples // batch_size

        for epoch in range(epochs):
            for _ in range(iterations_per_epoch):
                indices = np.random.choice(num_examples, size=batch_size, replace=False)
                X_batch = X[indices]
                y_batch = y[indices]

                hidden_layers, output_layer = self.forward_propagation(X_batch)

                self.backward_propagation(X_batch, y_batch, hidden_layers, output_layer)

            _, output = self.forward_propagation(X)
            cost = cross_entropy_loss(y, output)

    def predict(self, X):
        hidden_layers, output = self.forward_propagation(X)
        return np.argmax(output, axis=1)

# Loading and preprocessing the MNIST dataset
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(-1, 784) / 255.0
X_test = X_test.reshape(-1, 784) / 255.0

y_train_encoded = np.zeros((y_train.shape[0], 10))
y_train_encoded[np.arange(y_train.shape[0]), y_train] = 1

# Test different numbers of hidden layers
hidden_layer_sizes = [[20], [20, 20], [20, 20, 20], [20,20,20,20]]

for hidden_sizes in hidden_layer_sizes:
    mlp = MLP(input_size=784, hidden_sizes=hidden_sizes, output_size=10, learning_rate=0.01)
    mlp.train(X_train, y_train_encoded, epochs=250, batch_size=126)

    y_pred = mlp.predict(X_test)
    accuracy = np.mean(y_pred == y_test)
    print("Hidden Layers: {}, Accuracy: {:.2%}".format(len(hidden_sizes), accuracy))