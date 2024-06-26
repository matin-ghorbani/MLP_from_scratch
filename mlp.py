import numpy as np
from tqdm import tqdm


class Mlp:
    def __init__(self, dimension_input, dimension_output, H1, H2, epochs, lr,
                 act_func1, act_func2, act_func_output):

        self.dimension_input = dimension_input
        self.dimension_output = dimension_output

        self.H1 = H1
        self.H2 = H2

        self.epochs = epochs
        self.lr = lr

        self.act_func1 = act_func1
        self.act_func2 = act_func2
        self.act_func_output = act_func_output

        self.weight1 = np.random.randn(self.dimension_input, self.H1)
        self.weight2 = np.random.randn(self.H1, self.H2)
        self.weight3 = np.random.randn(self.H2, self.dimension_output)

        self.bias1 = np.random.randn(1, self.H1)
        self.bias2 = np.random.randn(1, self.H2)
        self.bias3 = np.random.randn(1, self.dimension_output)

    def activation_functions(self, func, x):
        if func == 'sigmoid':
            return 1 / (1 + np.exp(-x))

        if func == 'softmax':
            return np.exp(x) / np.sum(np.exp(x))

    def forward(self, x):
        x = x.reshape(-1, 1)

        # Layer 1
        out1 = self.activation_functions(
            self.act_func1, x.T @ self.weight1 + self.bias1)

        # Layer 2
        out2 = self.activation_functions(
            self.act_func2, out1 @ self.weight2 + self.bias2)

        # Layer 3
        out3 = self.activation_functions(
            self.act_func_output, out2 @ self.weight3 + self.bias3)

        return out3, out2, out1

    def back_propagation(self, out1, out2, out3, x_train, y_train):
        x_train = x_train.reshape(-1, 1)

        # Layer 3
        error = -2 * (y_train - out3)
        grad_weight3 = out2.T @ error
        grad_bias3 = error

        # Layer 2
        error = error @ self.weight3.T * out2 * (1 - out2)
        grad_weight2 = out1.T @ error
        grad_bias2 = error

        # Layer 1
        error = error @ self.weight2.T * out1 * (1 - out1)
        grad_weight1 = x_train @ error
        grad_bias1 = error

        return grad_weight1, grad_weight2, grad_weight3, grad_bias1, grad_bias2, grad_bias3

    def update(self, grad_weight1, grad_weight2, grad_weight3, grad_bias1, grad_bias2, grad_bias3):

        # Layer 1
        self.weight1 -= self.lr * grad_weight1
        self.bias1 -= self.lr * grad_bias1

        # Layer 2
        self.weight2 -= self.lr * grad_weight2
        self.bias2 -= self.lr * grad_bias2

        # Layer 3
        self.weight3 -= self.lr * grad_weight3
        self.bias3 -= self.lr * grad_bias3

    def fit(self, x_train, y_train):
        losses = []
        accuracies = []
        for _ in tqdm(range(self.epochs)):
            Y_pred = []
            # train
            for x, y in zip(x_train, y_train):
                out3, out2, out1 = self.forward(x)

                y_pred = out3
                Y_pred.append(y_pred)

                grad_W1, grad_W2, grad_W3, grad_B1, grad_B2, grad_B3 = self.back_propagation(
                    out1, out2, out3, x, y)

                self.update(grad_W1, grad_W2, grad_W3,
                            grad_B1, grad_B2, grad_B3)

            loss, accuracy = self.evaluate(x_train, y_train)
            losses.append(loss)
            accuracies.append(accuracy)

        return losses, accuracies

    def predict(self, x_test):
        y_pred = []
        for x in x_test:
            y_pred.append(self.forward(x)[0])

        y_pred = np.array(y_pred).reshape(-1, self.dimension_output)
        return y_pred

    def calc_loss(self, y_pred, y_test, metric='mse'):

        if metric == 'mse':
            loss = np.mean((y_pred - y_test) ** 2)
        elif metric == 'mae':
            loss = np.mean(np.abs(y_pred - y_test))
        elif metric == 'rmse':
            loss = np.sqrt(np.mean((y_pred - y_test) ** 2))
        else:
            raise Exception('Not supported metric')
        return loss

    def calc_accuracy(self, y_pred, y_test):
        accuracy = np.sum(np.argmax(y_test, axis=1) ==
                          np.argmax(y_pred, axis=1))/len(y_pred)
        return accuracy

    def evaluate(self, x_test, y_test):
        y_pred = self.predict(x_test)
        loss = self.calc_loss(y_pred, y_test)
        accuracy = self.calc_accuracy(y_pred, y_test)
        return loss, accuracy


if __name__ == '__main__':
    from sklearn.datasets import load_digits
    from sklearn.model_selection import train_test_split
    from OneHotEncoder_OneHotDecoder_classes import OneHotEncoder
    import matplotlib.pyplot as plt

    dataset = load_digits()

    X = dataset.data
    Y = dataset.target

    encoder = OneHotEncoder()
    encoder.fit(Y)
    Y = np.array(encoder.transform(Y))

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    model = Mlp(dimension_input=x_train.shape[1], dimension_output=y_train.shape[1], H1=128, H2=32,
                epochs=20, lr=.001, act_func1='sigmoid', act_func2='sigmoid', act_func_output='softmax')

    losses, accuracies = model.fit(x_train, y_train)

    loss_train, accuracy_train = model.evaluate(x_train, y_train)
    loss_test, accuracy_test = model.evaluate(x_test, y_test)

    print(f'loss_test: {loss_test}, accuracy_test: {accuracy_test}')
    print(f'loss_train: {loss_train}, accuracy_train: {accuracy_train}')
