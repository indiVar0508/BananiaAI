import numpy as np

class NeuralNet():

	def __init__(self, layers = [2, 2, 1], learningRate = 0.09, activationFunc = 'sigmoid', Gaussian = True):
		self.layers = layers
		self.learningRate = learningRate
		self.Gaussian = Gaussian
		if Gaussian:
			self.biasses = [np.random.randn(1, l) for l in self.layers[1:]] # n * 3
			self.weights = [np.random.randn(i, o) for i, o in zip(self.layers[:-1], self.layers[1:])] # n X 2 * 2 X 3 = n * 3
		else:
			self.biasses = [np.random.randn(1, l) for l in self.layers[1:]] # n * 3
			self.weights = [np.random.randn(i, o) for i, o in zip(self.layers[:-1], self.layers[1:])] # n X 2 * 2 X 3 = n * 3
		self.activationFunc = activationFunc

	def sigmoid(self, z):
		return (1 / (1. + np.exp(np.clip(-z, -708, 708))))

	def sigmoidPrime(self, z):
		return self.sigmoid(z) * (1 - self.sigmoid(z))

	def RelU(self, z):
		z[z<0] = 0
		return z
	def ReLUPrime(self, z):
		z[z!=0] = 1
		return z

	def feedForward(self, X):
		X = np.array(X).reshape(1, -1)
		assert self.layers[0] == X.shape[1]
		activations = [X]
		for w, b in zip(self.weights, self.biasses):
			try:
				if self.activationFunc == 'sigmoid': X = self.sigmoid(np.matmul(X, w) + b)
				elif self.activationFunc == 'relu': X = self.RelU(np.matmul(X, w) + b)
			except ValueError:
				print(X.shape, w.shape, b.shape, self.layers, len(activations))
				raise
			activations.append(X)
		return activations

	def softmax(self, z):
		exps = [np.exp(np.clip(e, -708, 708)) for e in z]
		sum_of_exps = np.sum(exps)
		softmax = [e / sum_of_exps for e in exps]
		return softmax

	def predict(self, X, show = 'probability'):
		if show == 'round': return np.round(self.softmax(self.feedForward(X)[-1]))
		elif show == 'softmax': 
			softmax = []
			preds = self.feedForward(X)[-1]
			for pred in preds: softmax.append(self.softmax(pred))
			return np.argmax(softmax, 1)
		elif show == 'probability': 
			softmax = []
			preds = self.feedForward(X)[-1]
			for pred in preds: softmax.append(self.softmax(pred))
			return softmax



	def backPropogate(self, x, y):
		bigDW = [np.zeros(w.shape) for w in self.weights]
		bigDB = [np.zeros(b.shape) for b in self.biasses]
		activations = self.feedForward(x)
		delta = activations[-1] - y
		for layer in range(2, len(self.layers) + 1):
			# print(bigDW[-layer + 1].shape, np.dot(activations[-layer].T, delta).shape)
			# print(delta.shape, self.weights[-layer + 1].shape)
			bigDW[-layer + 1] = (1 / len(x)) * np.dot(activations[-layer].T, delta)
			bigDB[-layer + 1] = (1 / len(x)) * np.sum(delta)
			if self.activationFunc == 'sigmoid': delta = np.dot(delta, self.weights[-layer + 1].T) * self.sigmoidPrime(activations[-layer])
			elif self.activationFunc == 'relu': delta = np.dot(delta, self.weights[-layer + 1].T) * self.ReLUPrime(activations[-layer])

		for w, dw in zip(self.weights, bigDW): w -= self.learningRate * dw
		for b, db in zip(self.biasses, bigDB): b -= self.learningRate * db


	def fit(self, x, y, epochs = 100):
		for _ in range(epochs): self.backPropogate(x, y)
