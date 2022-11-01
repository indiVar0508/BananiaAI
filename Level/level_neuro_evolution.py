import pygame

from Character.population import Population
from Level.level_one import Level

from Utility import ui

class LevelNeuroEvolution(Level):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs = 7
        self.population = Population(step=10, draw=False,
        layers = [[self.inputs, 10, 4],[self.inputs, 10, 10,4],
        [self.inputs, 6, 4],[self.inputs, 18, 4],
        [self.inputs, 20,  4],
        [self.inputs, 12, 4],
        [self.inputs, 5, 4], 
        [self.inputs, 3, 2, 4], 
        [self.inputs, 5, 7, 4], [self.inputs, 7, 4], [self.inputs, 8, 5, 4],[self.inputs, 12, 5, 4],
        [self.inputs, 10, 4]] ,\
        mutation = 0.2, populationSize = 100)

    def showVision(self, player, cords):
        self.handleVision(player)
        self.handleHurdleVision(player, cords)
        pygame.draw.line(self.gameDisplay, player.leftVision, (player.x + player.width // 2, player.y + player.length // 2), player.leftVisionBlock)
        pygame.draw.line(self.gameDisplay, player.rightVision, (player.x + player.width // 2, player.y + player.length // 2), player.rightVisionBlock)
        pygame.draw.line(self.gameDisplay, player.upVision, (player.x + player.width // 2, player.y + player.length // 2), player.upVisionBlock)
        pygame.draw.line(self.gameDisplay, player.downVision, (player.x + player.width // 2, player.y + player.length // 2), player.downVisionBlock)

    def contactingHurdle(self, player, cordinates):
        for cords in cordinates:
            if (cords[0] < player.x + 5 < cords[0] + cords[2] or cords[0] < player.x + player.width - 5 < cords[0] + cords[2]) and\
            (cords[1] < player.y + 5 < cords[1] + cords[3] or cords[1] < player.y + player.length - 5 < cords[1] + cords[3]): return True, cords
        return False, None

    def handleHurdleVision(self, player, cordinates):
        # player.leftVision = player.rightVision = player.upVision = player.downVision = (255, 255 ,255)
        for idx, cords in enumerate(cordinates):
            if player.x + player.width // 2 >= cords[0] + cords[2]  and cords[1] <= player.y + player.length // 2 <= cords[1] + cords[3] and player.x + player.width // 2 - (cords[0] + cords[2]) <= player.visionLimit:
                player.leftDistance = player.x + player.width // 2 - (cords[0] + cords[2])
                player.leftVisionBlock = (cords[0] + cords[2], player.y + player.length // 2)
                player.leftVision = (255, 0 , 0)
            elif player.x + player.width // 2 <= cords[0] and cords[1] <= player.y + player.length // 2 <= cords[1] + cords[3] and cords[0] - (player.x + player.width // 2) <= player.visionLimit:
                player.rightDistace =  cords[0] - (player.x + player.width // 2)
                player.rightVisionBlock = (cords[0], player.y + player.length // 2)
                player.rightVision = (255, 0 , 0)
            elif player.y + player.length // 2 >= cords[1] + cords[3] and cords[0] <= player.x + player.width // 2 <= cords[0] + cords[2] and player.y + player.length // 2 - (cords[1] + cords[3]) <= player.visionLimit:
                player.upDistance =  player.y + player.length // 2 - (cords[1] + cords[3])
                player.upVisionBlock = (player.x + player.width // 2, cords[1] + cords[3])
                player.upVision = (255, 0 , 0)
            elif player.y + player.length // 2 <= cords[1] and cords[0] <= player.x + player.width // 2 <= cords[0] + cords[2] and cords[1] - (player.y + player.length // 2) <= player.visionLimit:
                player.downDistance =  cords[1] - (player.y + player.length // 2)
                player.downVisionBlock = (player.x + player.width // 2, cords[1])
                player.downVision = (255, 0 , 0)


    def hurdleContact(self, player, cords):
        self.handleHurdleVision(player, cords)
        condn, cords = self.contactingHurdle(player, cords)
        if condn:
            player.fitness -= 0.00025
            if player.left: 
                player.x = cords[0] + cords[2] + 6
                player.left = False
                player.upVisionBlock = (player.upVisionBlock[0] + player.step, player.upVisionBlock[1])
                player.downVisionBlock = (player.downVisionBlock[0] + player.step, player.downVisionBlock[1])
            elif player.right: 
                player.x = cords[0] - player.width - 6
                player.right = False
                player.upVisionBlock = (player.upVisionBlock[0] - player.step, player.upVisionBlock[1])
                player.downVisionBlock = (player.downVisionBlock[0] - player.step, player.downVisionBlock[1])
            elif player.up: 
                player.y = cords[1] + cords[3] + 6
                player.up = False
                player.leftVisionBlock = (player.leftVisionBlock[0], player.leftVisionBlock[1] + player.step)
                player.rightVisionBlock = (player.rightVisionBlock[0], player.rightVisionBlock[1] + player.step)
            elif player.down: 
                player.y = cords[1] - player.length	- 6
                player.down = False
                player.leftVisionBlock = (player.leftVisionBlock[0], player.leftVisionBlock[1] - player.step)
                player.rightVisionBlock = (player.rightVisionBlock[0], player.rightVisionBlock[1] - player.step)


    def handleVision(self, player):
        player.leftVision = player.rightVision = player.upVision = player.downVision = (255, 255 ,255)
        if (player.x + player.width // 2) - player.visionLimit < 0: 
            player.leftVisionBlock = (0, player.y + player.length // 2)
            player.leftVision = (255, 0, 0)
            player.leftDistance = player.x + player.width // 2
        else: 
            player.leftVisionBlock = (player.x + player.width // 2 - player.visionLimit, player.y + player.length // 2)
            player.leftDistance = player.visionLimit

        if player.x + player.width // 2 + player.visionLimit > self.gameDimension[0]: 
            player.rightVisionBlock = (self.gameDimension[0], player.y + player.length // 2)
            player.rightVision = (255, 0, 0)
            player.rightDistace =  self.gameDimension[0] - (player.x + player.width // 2)
        else: 
            player.rightDistace = player.visionLimit
            player.rightVisionBlock = (player.x + player.width // 2 + player.visionLimit, player.y + player.length // 2)

        if player.y + player.length // 2 - player.visionLimit < 0: 
            player.upDistance =  player.y + player.length // 2
            player.upVisionBlock = (player.x + player.width // 2, 0)
            player.upVision = (255, 0, 0)
        else: 
            player.upDistance = player.visionLimit
            player.upVisionBlock = (player.x + player.width // 2, player.y + player.length // 2 - player.visionLimit)

        if player.y + player.length // 2 + player.visionLimit > self.gameDimension[1]: 
            player.downDistance =   self.gameDimension[1] - (player.y + player.length // 2)
            player.downVisionBlock = (player.x + player.width // 2, self.gameDimension[1])
            player.downVision = (255, 0, 0)
        else: 
            player.downDistance = player.visionLimit
            player.downVisionBlock = (player.x + player.width // 2, player.y + player.length // 2 + player.visionLimit)

    def show_population(self, foodCords, hurdleCords):
        for player in self.population.players:
            if player.alive:
                player.getFitness(foodCords, hurdleCords)
                # print(self.alivePopulation)
                # player.fitness += 0.00005
                self.player = player
                self.dynamics()
                self.collision()
                self.show_player(draw=False)
                self.showVision(player, self.hurdle_cords)
                player.position.append((player.x, player.y))
                # for img in images: 
                # 	for i in img: 
                # 		# print(i)
                # 		self.gameDisplay.blit(i[0], (player.x, player.y))
                # 		player.showVision()
                # 		if i[1]: break
                if not player.isAlive(hurdleCords): self.population.alivePopulation -= 1


    def start_game(self, *args):
        # self.pause_game()

        while True:
            while not self.population.allDead(): ######
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                self.population.think(self.food_cords[0])
                self.show_game()
                self.show_population(self.food_cords[0], self.hurdle_cords)
                # if self.population.allDead(): print('done')
                ui.message(self.gameDisplay, msg = 'Generation : {} Alive : {}'.format(self.population.generation, self.population.alivePopulation), color = (250, 250, 250))
                pygame.display.update()
                # if self.population.allDead(): print('aakhri')
                # pygame.time.wait(240)
            # print('evolving', self.population.alivePopulation)
            self.population.evolve()

            # print('evolved')
