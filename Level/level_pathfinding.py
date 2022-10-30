import pygame
import numpy as np
from collections import OrderedDict
from Level.level_one import Level

class Level_PathFinding(Level):

    def __init__(self, player, **kwargs):
        super().__init__(player, **kwargs)
        self.wall = np.zeros((self.gameDimension[1] // 10, self.gameDimension[0] // 10))
        for hurdle in self.hurdle:
            for x in range(hurdle.x // 10, hurdle.x // 10 + hurdle.width // 10):
                for y in range(hurdle.y // 10, hurdle.y // 10 + hurdle.length // 10):
                    self.wall[y, x] = 1
                    self.wall[y - 1, x] = 1
                    self.wall[y - 2, x] = 1
                    # self.wall[y - 3, x] = 1

                    self.wall[y, x - 1] = 1
                    self.wall[y, x - 2] = 1
                    self.wall[y, x - 3] = 1

                    self.wall[y - 1, x - 1] = 1
                    self.wall[y - 2, x - 2] = 1
                    # self.wall[y - 3, x - 3] = 1

        self.f_score = np.full(self.wall.shape, np.inf)
        self.g_score = np.zeros(self.wall.shape)
        self.not_visited = list()
        self.visited = list()
        self.neighbour = OrderedDict()
        self.came_from = OrderedDict()
        self.cur_idx =None

        for i in range(self.wall.shape[0]):
            for j in range(self.wall.shape[1]):
                self.neighbour[(i, j)] = self.get_neighbours(i, j)

        self.start_pos = (self.player.y // 10, self.player.x // 10)
        self.end_pos = (self.food_cords[0].y // 10, self.food_cords[0].x // 10)

    def get_neighbours(self, i, j):
        possible_neighbours = []
        if i > 0:
            possible_neighbours.append((i-1, j))
        if i < self.wall.shape[0] - 1:
            possible_neighbours.append((i + 1, j))
        if j > 0:
            possible_neighbours.append((i, j - 1))
        if j < self.wall.shape[1] - 1:
            possible_neighbours.append((i, j + 1))
        # if i > 0 and j > 0:
        #     possible_neighbours.append((i-1, j-1))
        # if i < self.wall.shape[0] - 1 and j < self.wall.shape[1] - 1:
        #     possible_neighbours.append((i + 1, j+1))
        # if j > 0 and i < self.wall.shape[0] - 1:
        #     possible_neighbours.append((i+1, j - 1))
        # if j < self.wall.shape[1] - 1 and i > 0:
        #     possible_neighbours.append((i-1, j + 1))
        return possible_neighbours

    def find_path_a_star(self):
        self.not_visited += [self.start_pos]
        while len(self.not_visited) > 0:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            cur_idx = self.not_visited[0]
            for i, j in self.not_visited:
                if self.f_score[(i, j)] < self.f_score[cur_idx]:
                    cur_idx = (i, j)

            if cur_idx == self.end_pos:
                # pygame.time.wait(3000)
                self.cur_idx = cur_idx
                return

            self.not_visited.remove(cur_idx)
            self.visited.append(cur_idx)

            for neighbour in self.neighbour[cur_idx]:
                if neighbour not in self.visited and self.wall[neighbour] == 0:
                    estimated_g_score = self.g_score[neighbour] + 10

                    if neighbour not in self.not_visited:
                        self.not_visited.append(neighbour)
                    elif self.g_score[neighbour] < estimated_g_score:
                        continue

                    self.g_score[neighbour] = estimated_g_score
                    # self.f_score[neighbour] = estimated_g_score + (abs(self.end_pos[0] - neighbour[0])*10 +
                    #                                                abs(self.end_pos[1] - neighbour[1])*10)
                    self.f_score[neighbour] = estimated_g_score + np.sqrt((self.end_pos[0]*10 - neighbour[0]*10)**2 +
                                                                   (self.end_pos[1]*10 - neighbour[1]*10)**2)
                    self.came_from[neighbour] = cur_idx

            self.show(cur_idx)
            pygame.display.update()
            self.clock.tick(30)
        print("No Path")

    def draw_grids(self, current):
        for point in self.not_visited:
            pygame.draw.rect(self.gameDisplay, (200, 200, 200), (point[1] * 10, point[0] * 10, 10, 10))
        for point in self.visited:
            pygame.draw.rect(self.gameDisplay, (120, 120, 120), (point[1] * 10, point[0] * 10, 10, 10))

        to_draw = list()
        to_draw.append(current)
        while current in self.came_from.keys():
            current = self.came_from[current]
            to_draw.append(current)

        for point in to_draw:
            pygame.draw.rect(self.gameDisplay, (0, 0, 250), (point[1] * 10, point[0] * 10, 10, 10))
        for x in range(0, self.gameDimension[0], 10):
            pygame.draw.line(self.gameDisplay, self.grid_lines, (x, 0), (x, self.gameDimension[1]))
        for y in range(0, self.gameDimension[1], 10):
            pygame.draw.line(self.gameDisplay, self.grid_lines, (0, y), (self.gameDimension[0], y))

    # def draw_grids_path(self, current):
    #     for point in self.not_visited:
    #         pygame.draw.rect(self.gameDisplay, (0, 200, 0), (point[0] * 10, point[1] * 10, 10, 10))
    #     for point in self.visited:
    #         pygame.draw.rect(self.gameDisplay, (255, 0, 0), (point[0] * 10, point[1] * 10, 10, 10))
    #
    #     to_draw = list()
    #     to_draw.append(current)
    #     while current in self.came_from.keys():
    #         current = self.came_from[current]
    #         to_draw.append(current)
    #
    #     for point in to_draw:
    #         pygame.draw.rect(self.gameDisplay, (0, 0, 250), (point[0] * 10, point[1] * 10, 10, 10))


    def start_game(self):

        # self.pause_game()
        self.find_path_a_star()
        current = self.cur_idx
        prev = current
        # 0 - l, 1 - r, 2 - u, 3 - d
        moves = []
        c = 0
        while current in self.came_from.keys():
            c += 1
            current = self.came_from[current]
            if current[0] > prev[0] and current[1] == prev[1]:
                moves.insert(0, 2)
            if current[0] < prev[0] and current[1] == prev[1]:
                moves.insert(0, 3)

            if current[1] < prev[1] and current[0] == prev[0]:
                moves.insert(0, 1)
            if current[1] > prev[1] and current[0] == prev[0]:
                moves.insert(0, 0)

            prev = current

        move_idx = 0
        while self.player.alive and not self.player.gotFood and move_idx < len(moves):

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_p:
                        self.pause_game()

            if moves[move_idx] == 0:
                self.player.left = True
                self.player.right = self.player.up = self.player.down = False

            if moves[move_idx] == 1:
                self.player.right = True
                self.player.left = self.player.up = self.player.down = False

            if moves[move_idx] == 2:
                self.player.up = True
                self.player.right = self.player.left = self.player.down = False

            if moves[move_idx] == 3:
                self.player.down = True
                self.player.right = self.player.up = self.player.left = False

            self.show(self.cur_idx)
            pygame.draw.rect(self.gameDisplay, (200, 250,190), (self.player.x,self.player.y, 10, 10))
            self.dynamics()
            self.collision()
            pygame.display.flip()
            if self.screen_capt:
                self.read_screen(stream=self.stream, gray=self.gray, maxi=self.maxi, store=self.store,
                                 player=self.player, vision_limit=50)
            self.clock.tick(30)
            move_idx += 1
        if self.player.alive and self.player.gotFood:
            self.have_won(self.cur_idx)

        pygame.time.wait(5_000)
