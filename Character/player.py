import os
import pygame
from Utility.shape import Rectangle


class Player(Rectangle):

    def __init__(self, step, draw=False, **kwargs):
        super().__init__(**kwargs)
        self.step = step
        self.left = self.right = self.up = self.down = False
        self.alive = True
        self.gotFood = False
        self.draw = draw
        if not draw:
            self.characterDefault = pygame.transform.scale(pygame.image.load(r'Resources/Character/StandBy/1.png'),
                                                           (self.width, self.length))
            self.winDefault = pygame.transform.scale(pygame.image.load(r'Resources/Character/StandBy/2.png'),
                                                           (self.width, self.length))
            movements = os.path.join(r"Resources/Character/Movements")
            self.movements = {}
            movements_type = ['Left', 'Right', 'Down', 'Up']
            for m_type in movements_type:
                path = os.path.join(movements, f"{m_type}Movement")
                self.movements[m_type] = {}
                for file in os.listdir(path):
                    self.movements[m_type][int(file.split(".")[0]) - 1] = pygame.transform.scale(
                        pygame.image.load(os.path.join(path, file)), (self.width, self.length))
            self.l_img = self.r_img = self.u_img = self.d_img = 0

    def move(self):
        if self.left:
            self.x -= self.step
        elif self.right:
            self.x += self.step
        elif self.up:
            self.y -= self.step
        elif self.down:
            self.y += self.step
        
