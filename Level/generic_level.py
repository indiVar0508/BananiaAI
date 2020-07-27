import os
import cv2
import pygame
import numpy as np
from PIL import ImageGrab
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
    def pause_game(self):
        pass

    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def dynamics(self):
        pass

    @abstractmethod
    def collision(self):
        pass

    @abstractmethod
    def have_won(self):
        pass

    @abstractmethod
    def have_died(self):
        pass

    @staticmethod
    def make_obj_msg(msg, font_definition, color=(0, 0, 0)):
        msg_obj = font_definition.render(msg, True, color)
        return msg_obj, msg_obj.get_rect()

    def draw_grids(self):
        for x in range(0, self.gameDimension[0], 10):
            pygame.draw.line(self.gameDisplay, self.grid_lines, (x, 0), (x, self.gameDimension[1]))
        for y in range(0, self.gameDimension[1], 10):
            pygame.draw.line(self.gameDisplay, self.grid_lines, (0, y), (self.gameDimension[0], y))

    def message(self, msg, color=(0, 0, 0), font_type='freesansbold.ttf', font_size=15, x=10, y=10):
        font_definition = pygame.font.Font(font_type, font_size)
        msg_surface, msg_rectangle = self.make_obj_msg(msg, font_definition, color)
        msg_rectangle = (x, y)
        self.gameDisplay.blit(msg_surface, msg_rectangle)

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
