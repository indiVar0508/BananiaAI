import numpy as np
from copy import deepcopy
from collections import deque
from Character.player import Player
from Character.brain.brain import MutableBrain

class MutablePlayer(Player):

	def __init__(self, step, draw=False, layers = [4, 2, 4], learningRate = 0.09, activationFunc = 'relu', Gaussian = False, weights = None, biasses = None, **kwargs):
		super().__init__(step, draw, **kwargs)
		self.Brain = MutableBrain(layers = layers, learningRate = learningRate, activationFunc = activationFunc, Gaussian = Gaussian, weights = weights, biasses = biasses)
		self.steps = 500_000
		self.visionLimit = 70
		self.leftVision = self.rightVision = self.upVision = self.downVision = (255, 255 ,255)
		self.leftVisionBlock = (self.x + self.width // 2 - self.visionLimit, self.y + self.length // 2)
		self.rightVisionBlock = (self.x + self.width // 2 + self.visionLimit, self.y + self.length // 2)
		self.upVisionBlock = (self.x + self.width // 2, self.y + self.length // 2 - self.visionLimit)
		self.downVisionBlock = (self.x + self.width // 2, self.y + self.length // 2 + self.visionLimit)
		self.leftDistance = self.rightDistace = self.upDistance = self.downDistance = self.visionLimit
		self.fitness = 0.0 #score
		self.position = deque(maxlen=50)

	def isAlive(self, hurdles):
		# print(self.fitness)

		if ((len(self.position) == 50) and (len(set(self.position)) == 1)):
			self.alive = False
			self.fitness -= 100
			return False

		if (self.steps < 0) or (self.steps < 8000 and self.x < hurdles[0][0]) \
		or (self.steps < 7000 and (hurdles[0][0] < self.x < hurdles[1][0]))\
		or (self.steps < 5000 and (hurdles[1][0] < self.x < hurdles[3][0]))\
		or (self.steps < 4000 and (hurdles[3][0] < self.x < hurdles[4][0])) \
		or (self.steps < 2000 and (hurdles[4][0] < self.x < hurdles[6][0]))\
		or (self.steps < 1000 and (hurdles[6][0] < self.x < hurdles[8][0])): 
			self.alive = False
			self.fitness -= 10
			return False
		# if :
			# self.alive = False
			# return False
		return True

	def got_food(self, foodLoc):
		if (foodLoc.x <= self.x <= foodLoc.x + foodLoc.width or foodLoc.x <= self.x + self.width <= foodLoc.x + foodLoc.width) \
		and (foodLoc.y <= self.y <= foodLoc.y + foodLoc.length or foodLoc.y <= self.y + self.height <= foodLoc.y + foodLoc.length):
			self.alive = False
			# print('Yeah.!')
			# print(self.Brain.layers)
			return 100
		return 1


	def getFitness(self, foodCords, hurdles):
		self.fitness += (1 / abs(self.x - foodCords.x))
		i = len(hurdles) - 2
		while i >= 0 and hurdles[i][0] > self.x: i -= 1
		self.fitness += (1 / (abs(self.y - hurdles[i+1][1]) +1))
		self.fitness += i * 10 + self.got_food(foodCords)
		self.fitness += (1 / (self.steps + 2))
		if not (self.up or self.down or self.left or self.right):
			self.fitness -= 1

	def biCrossOver(parentOne, parentTwo):
		child = MutablePlayer(step = parentOne.step, draw= parentOne.draw, layers = deepcopy(parentOne.Brain.layers), \
			activationFunc = parentOne.Brain.activationFunc, Gaussian = parentTwo.Brain.Gaussian,\
				weights = deepcopy(parentOne.Brain.weights), biasses = deepcopy(parentTwo.Brain.biasses))
		for idx, _ in enumerate(child.Brain.weights):
			for row, __ in enumerate(child.Brain.weights[idx]):
				for col, ___ in enumerate(child.Brain.weights[idx][row]):
					if np.random.random() < 0.5: child.Brain.weights[idx][row][col] = np.copy(parentOne.Brain.weights[idx][row][col])
					else: child.Brain.weights[idx][row][col] = np.copy(parentTwo.Brain.weights[idx][row][col])
		for idx, _ in enumerate(child.Brain.biasses):
			for row, __ in enumerate(child.Brain.biasses[idx]):
				for col, ___ in enumerate(child.Brain.biasses[idx][row]):
					if np.random.random() < 0.5: child.Brain.biasses[idx][row][col] = np.copy(parentOne.Brain.biasses[idx][row][col])
					else: child.Brain.biasses[idx][row][col] = np.copy(parentTwo.Brain.biasses[idx][row][col])

		return child

	def uniCrossOver(parentOne):
		child = MutablePlayer(step = parentOne.step, draw = parentOne.draw, layers = deepcopy(parentOne.Brain.layers), \
			activationFunc = parentOne.Brain.activationFunc, Gaussian = parentOne.Brain.Gaussian,\
				weights = None, biasses = None)
		for idx, _ in enumerate(child.Brain.weights):
			if np.random.random() < 0.5:
				child.Brain.weights[idx] = np.copy(parentOne.Brain.weights[idx])
			if np.random.random() < 0.5:
				child.Brain.biasses[idx] = np.copy(parentOne.Brain.biasses[idx])
		return child



	def think(self, foodCords):
		# foodDistance = abs(self.x - foodCords[0]) / self.gameWidth
		if self.left:
			horizontal = 1
			direction = 1
		elif self.right:
			horizontal = 1
			direction = -1
		elif self.up:
			horizontal = 0
			direction = 1
		elif self.down:
			horizontal = 0
			direction = -1
		else:
			horizontal = 0
			direction = 0

		state = np.array([1-(self.leftDistance / self.visionLimit), 1-(self.rightDistace / self.visionLimit), 1-(self.upDistance / self.visionLimit), 1-(self.downDistance / self.visionLimit),\
						horizontal, direction, self.fitness, self.x / 700, self.y / 400])
		
		action = self.Brain.predict(X = state, show = 'softmax')[0]
		# print(state, '-> ', action)
		if np.random.random() < 0.05:
			if action == 0: 
				self.up = True
				self.left = self.right = self.down = False
			elif action == 1:
				self.down = True
				self.left = self.right = self.up = False
			elif action == 2:
				self.left = True
				self.right = self.up = self.down = False
			elif action == 3:
				self.right = True
				self.left = self.up = self.down = False
		else:
			action = np.random.randint(4)
		self.steps -= 10
		
