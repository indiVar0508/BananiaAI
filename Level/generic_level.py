import os
try:
    import cv2
    from PIL import ImageGrab
except:
    pass
import pygame
import numpy as np
from abc import ABC, abstractmethod
pygame.init()

ux, uy = (50, 50)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (ux, uy)


class GenericLevel(ABC):

    def __init__(self, game_dimension, screen_capt, stream, gray, maxi, store):
        self.gameDisplay = pygame.display.set_mode(game_dimension)
        self.gameDimension = game_dimension
        self.background = (165, 20, 20)
        self.grid_lines = (5, 5, 5)
        self.clock = pygame.time.Clock()
        self.frames = []
        self.screen_capt = screen_capt
        self.stream = stream
        self.gray = gray
        self.maxi = maxi
        self.store = store

    @abstractmethod
    def pause_game(self, *args):
        pass

    @abstractmethod
    def start_game(self, *args):
        pass

    @abstractmethod
    def show(self, *args):
        pass

    @abstractmethod
    def dynamics(self, *args):
        pass

    @abstractmethod
    def collision(self, *args):
        pass

    @abstractmethod
    def have_won(self, *args):
        pass

    @abstractmethod
    def have_died(self, *args):
        pass

    def draw_grids(self, *args):
        for x in range(0, self.gameDimension[0], 10):
            pygame.draw.line(self.gameDisplay, self.grid_lines, (x, 0), (x, self.gameDimension[1]))
        for y in range(0, self.gameDimension[1], 10):
            pygame.draw.line(self.gameDisplay, self.grid_lines, (0, y), (self.gameDimension[0], y))

    def give_me_pix(self, maxi=False, player=None, vision_limit=None):
        if not maxi:
            assert player is not None and vision_limit is not None
            x = 1.5 * (ux + player.x) - 3 * vision_limit
            y = 1.5 * (uy + player.y) - 3 * vision_limit
            width = 1.5 * (ux + player.x) + 3 * vision_limit
            height = 1.5 * (uy + player.y) + 3 * vision_limit
            if x < 1.5 * ux:
                x = 1.5 * ux
                width = 1.5 * ux + 6 * vision_limit
            elif width > 1.5 * (ux + self.gameDimension[0]):
                x = 1.5 * (ux + self.gameDimension[0]) - 6 * vision_limit
                width = x + 6 * vision_limit
            if y < 1.5 * uy:
                y = 1.5 * uy
                height = 1.5 * uy + 6 * vision_limit
            elif height > 1.5 * (uy + self.gameDimension[1]):
                y = 1.5 * (uy + self.gameDimension[1]) - 6 * vision_limit
                height = y + 6 * vision_limit
            return x, y, width, height
        return 1.5*ux, 1.5*uy, 1.5 * (ux+self.gameDimension[0]), 1.5 * (uy+self.gameDimension[1])

    def read_screen(self, stream=False, gray=False, maxi=False, store=False, player=None, vision_limit=None):
        screen = np.array(ImageGrab.grab(bbox=self.give_me_pix(maxi, player, vision_limit)))
        if gray:
            gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            if store:
                self.frames.append(gray)
            if stream:
                cv2.imshow('Streaming', gray)
        else:
            rgb = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            if store:
                self.frames.append(rgb)
            if stream:
                cv2.imshow('Streaming', rgb)
