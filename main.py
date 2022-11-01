import pygame
from Utility import ui
from Level.level_one import Level
from Level.level_pathfinding import Level_PathFinding
from Level.level_neuro_evolution import LevelNeuroEvolution
from Character.player import Player


class Main:

    def __init__(self):
        self.player = Player(step=10, draw=False, x=30, y=200, length=30, width=30, color=(230, 220, 50))
        self.gameDimension = (700, 400)
        self.gameDisplay = pygame.display.set_mode(self.gameDimension)
        self.clock = pygame.time.Clock()
        self.resume = False
        # self.level = Level_PathFinding(self.player, game_dimension=self.gameDimension, screen_capt=False, stream=False,
        #                    gray=False, maxi=False, store=False))

    def pause_game(self, *args):
        self.resume = False
        while not self.resume:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.resume = True

            self.gameDisplay.fill((180, 180, 180))
            ui.message(gameDisplay=self.gameDisplay, msg="Welcome, select your option !", x=self.gameDimension[0] // 2 - 80, y=30 )
            ui.button(gameDisplay=self.gameDisplay, message="Play yourself", x=self.gameDimension[0] // 2 - 330, y=100, width=300, height=40,
                      inactive_color=(100,101,112), active_color=(50,50,56), action=lambda : self.initiate_level(Level))
            ui.button(gameDisplay=self.gameDisplay, message="A* Algorithm", x=self.gameDimension[0] // 2 - 330, y=150, width=300, height=40,
                      inactive_color=(100,101,112), active_color=(50,50,56), action=lambda : self.initiate_level(Level_PathFinding))

            # to be activated
            ui.button(gameDisplay=self.gameDisplay, message="BFS Algorithm(to be enabled)", x=self.gameDimension[0] // 2 - 330, y=200, width=300, height=40,
                      inactive_color=(211,211,213), active_color=(211,211,213), action=None)

            # to be activated
            ui.button(gameDisplay=self.gameDisplay, message="DFS Algorithm(to be enabled)", x=self.gameDimension[0] // 2 - 330, y=250, width=300, height=40,
                      inactive_color=(211,211,213), active_color=(211,211,213), action=None)

            # to be activated
            ui.button(gameDisplay=self.gameDisplay, message="Dijkstra's Algorithm(to be enabled)", x=self.gameDimension[0] // 2 - 330, y=300, width=300, height=40,
                      inactive_color=(211,211,213), active_color=(211,211,213), action=None)
            # to be activated
            ui.button(gameDisplay=self.gameDisplay, message="Neuro Evolution", x=self.gameDimension[0] // 2 + 30, y=100, width=300, height=40,
                      inactive_color=(100,101,112), active_color=(50,50,56), action=lambda: self.initiate_level(LevelNeuroEvolution))
            # to be activated
            ui.button(gameDisplay=self.gameDisplay, message="DQN(to be enabled)", x=self.gameDimension[0] // 2 + 30, y=150, width=300, height=40,
                      inactive_color=(211,211,213), active_color=(211,211,213), action=None)
            pygame.display.update()
            self.clock.tick(30)

    def initiate_level(self, level):
        self.level =  level(self.player, game_dimension=self.gameDimension, screen_capt=False, stream=False,
                           gray=False, maxi=False, store=False)
        self.resume=True

    def start(self):
        self.pause_game()
        self.level.start_game()


if __name__ == "__main__":
    main = Main()
    main.start()
