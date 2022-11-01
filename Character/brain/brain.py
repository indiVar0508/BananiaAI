import numpy as np
from collections import deque
from Character.brain.myneuralnet import NeuralNet


class mutableBrain(NeuralNet):

	def __init__(self, layers = [2, 2, 1], learningRate = 0.09, activationFunc = 'relu', Gaussian = False, weights = None, biasses = None):
		super().__init__(layers, learningRate, activationFunc, Gaussian)
		if weights != None: self.weights = weights
		if biasses != None: self.biasses = biasses

	def mutate(self, mutationRate = 0.01):
		for i in range(len(self.weights)):
			for row in range(len(self.weights[i])):
				for col in range(len(self.weights[i][row])):
					if np.random.random() < mutationRate: 
						if self.Gaussian: self.weights[i][row][col] = np.random.randn()
						else: self.weights[i][row][col] = np.random.random()
		for i in range(len(self.biasses)):
			for row in range(len(self.biasses[i])):
					if np.random.random() < mutationRate: 
						if self.Gaussian: self.biasses[i][row] = np.random.randn()
						else: self.biasses[i][row] = np.random.random()

	def giveMeChildBrainBY(parent):
		return mutableBrain(layers = parent.layers, learningRate = parent.learningRate, activationFunc = parent.activationFunc, Gaussian = parent.Gaussian,\
					 weights = parent.weights, biasses = parent.biasses)

# class QBrain:
# 	def __init__(self, layers = [2, 2, 1], learningRate = 0.09, activationFunc = 'relu', Gaussian = False, gamma = 0.9, epsilon = 1.0, epsilonDecay = 0.995, min_epsilon = 0.1):
# 		self.brain = NeuralNet(layers = layers, learningRate =learningRate, activationFunc = activationFunc, Gaussian = Gaussian)
# 		self.epsilon = epsilon
# 		self.gamma = 0.9
# 		self.epsilonDecay = epsilonDecay
# 		self.min_epsilon = min_epsilon
# 		self.memory = deque(maxlen = 20_000)
# 		self.stateSize = layers[0]
# 		self.actionSize = layers[-1]


# 	def remember(self, state, action, reward, next_state, done):
# 		self.memory.append((state, action, reward, next_state, done))

# 	def act(self, X):
# 		if np.random.random() < self.epsilon: return np.random.randint(self.actionSize)
# 		return self.brain.predict(X = X, show = 'softmax')

# 	def replay(self, batch_size):

# 		minibatch = np.random.sample(self.memory, batch_size)
# 		for state, action, reward, next_state, done in minibatch:
# 			target = reward
# 			if not done:
# 				target = (reward + self.gamma * np.amax(self.brain.predict(X = next_state, show = 'probability')))
# 			target_f = self.brain.predict(X = state, show = 'probability')
# 			target_f[0][action] = target
# 			self.brain.backPropogate(state, target_f)
# 		if self.epsilon > self.min_epsilon: self.epsilon *= self.epsilonDecay			





if __name__ == '__main__':
	nn = mutableBrain(layers = [2, 2, 2], learningRate = 0.25, activationFunc = 'relu', Gaussian = False)
	datasetX = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
	datasetY = [[1 - (x[0] ^ x[1]), x[0] ^ x[1]] for x in datasetX]
	print(datasetY)
	print(nn.predict(datasetX, show = 'probability'))
	print(nn.predict(datasetX, show = 'softmax'))
	nn.fit(datasetX, datasetY, epochs = 1000)
	print(nn.predict(datasetX, show = 'probability'))
	print(nn.predict(datasetX, show = 'softmax'))

