import pygame
from Level.generic_level import GenericLevel
from Utility.shape import Rectangle

class Level(GenericLevel):

    def __init__(self, player, **kwargs):
        super().__init__(**kwargs)
        self.player = player
        self.hurdle_cords = [
                             (130, 30, 30, self.gameDimension[1] - 60),
                             (200, 0, 30, self.gameDimension[1] // 2 - 20),
                             (200, self.gameDimension[1] // 2 + 20, 30, self.gameDimension[1] // 2 - 15)
                             ]

        for i in range(1, 3):
            self.hurdle_cords.append((130 + i * 180, 30, 30, self.gameDimension[1] - 60))
            self.hurdle_cords.append((130 + i * 180 + 70, 0, 30, self.gameDimension[1] // 2 - 20))
            self.hurdle_cords.append((130 + i * 180 + 70, self.gameDimension[1] // 2 + 20,
                                      30, self.gameDimension[1] // 2 - 15))

        self.hurdle = [Rectangle(x, y, l, w, (190, 220, 220)) for x, y, w, l in self.hurdle_cords]

        self.food_exists = True
        self.food_cords = [Rectangle(x=640, y=190, length=30, width=30, color=None)]
        self.food = pygame.transform.scale(pygame.image.load(r"Resources/Food/banana.png"), (self.food_cords[0].width,
                                                                                             self.food_cords[0].length))

    def draw_hurdle(self):
        for hurdle in self.hurdle:
            pygame.draw.rect(self.gameDisplay, hurdle.color, (hurdle.x, hurdle.y, hurdle.width, hurdle.length))
            size = hurdle.length // hurdle.width
            for y in range(size):
                pygame.draw.line(self.gameDisplay, self.grid_lines, (hurdle.x, hurdle.y + y*hurdle.width),
                                 (hurdle.x + hurdle.width, hurdle.y + y*hurdle.width))
                pygame.draw.circle(self.gameDisplay, (220, 50, 50), (hurdle.x + 15, hurdle.y + y*hurdle.width + 15), 3)
                pygame.draw.circle(self.gameDisplay, (220, 239, 0), (hurdle.x + 15, hurdle.y + y * hurdle.width + 15),
                                   1)

    def show_player(self, draw=True):
        if draw:
            pygame.draw.rect(self.gameDisplay, self.player.color,
                         (self.player.x, self.player.y, self.player.length, self.player.length))
            return
        blit_img = self.player.characterDefault
        if not (self.player.left or self.player.right or self.player.up or self.player.down):
            blit_img = self.player.characterDefault
            self.player.r_img = self.player.u_img = self.player.d_img = self.player.l_img = 0

        elif self.player.left:
            blit_img = self.player.movements['Left'][self.player.l_img]
            self.player.l_img = (self.player.l_img + 1) % 4
            self.player.r_img = self.player.u_img = self.player.d_img = 0
        elif self.player.right:
            blit_img = self.player.movements['Right'][self.player.r_img]
            self.player.r_img = (self.player.r_img + 1) % 4
            self.player.l_img = self.player.u_img = self.player.d_img = 0
        elif self.player.up:
            blit_img = self.player.movements['Up'][self.player.u_img]
            self.player.u_img = (self.player.u_img + 1) % 4
            self.player.r_img = self.player.l_img = self.player.d_img = 0
        elif self.player.down:
            blit_img = self.player.movements['Down'][self.player.d_img]
            self.player.d_img = (self.player.d_img + 1) % 4
            self.player.r_img = self.player.u_img = self.player.l_img = 0
        self.gameDisplay.blit(blit_img, (self.player.x, self.player.y))

    def draw_food(self):
        if self.food_exists:
            self.gameDisplay.blit(self.food, (self.food_cords[0].x, self.food_cords[0].y))

    def show(self):
        self.gameDisplay.fill(self.background)
        self.draw_grids()
        self.draw_hurdle()
        self.draw_food()
        self.show_player(draw=self.player.draw)

    def pause_game(self):
        resume = False
        while not resume:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        resume = True

            self.gameDisplay.fill((255, 255, 255))
            self.message(msg="Press, S to Start", x=self.gameDimension[0] // 2 - 50, y=self.gameDimension[1] // 2)
            pygame.display.update()
            self.clock.tick(30)

    def dynamics(self):
        self.player.move()

    def wall_logic(self):
        if self.player.x < 0:
            self.player.x = 0
            self.player.left = False
        elif self.player.x + self.player.width > self.gameDimension[0]:
            self.player.x = self.gameDimension[0] - self.player.width
            self.player.right = False

        if self.player.y < 0:
            self.player.y = 0
            self.player.up = False
        elif self.player.y + self.player.length > self.gameDimension[1]:
            self.player.y = self.gameDimension[1] - self.player.length
            self.player.down = False

    def hurdle_contact(self, blocks):
        for hurdle in blocks:
            if hurdle.x > self.player.x + self.player.width:
                continue

            if ((hurdle.x < self.player.x + self.player.width < hurdle.x + hurdle.width)
                    or (hurdle.x < self.player.x < hurdle.x + hurdle.width)
                    or (hurdle.x < self.player.x + self.player.width // 2 < hurdle.x + hurdle.width)) \
                    and \
                    ((hurdle.y < self.player.y + self.player.length < hurdle.y + hurdle.length)
                        or (hurdle.y < self.player.y < hurdle.y + hurdle.length)
                        or (hurdle.y < self.player.y + self.player.length // 2 < hurdle.y + hurdle.length)):
                return hurdle
        return None

    def hurdle_logic(self):
        cord = self.hurdle_contact(self.hurdle)
        if cord is None:
            return

        if self.player.right:
            self.player.x = cord.x - self.player.width
            self.player.right = False
        elif self.player.left:
            self.player.x = cord.x + cord.width
            self.player.left = False

        if self.player.down:
            self.player.y = cord.y - self.player.length
            self.player.down = False
        elif self.player.up:
            self.player.y = cord.y + cord.length
            self.player.up = False

    def food_logic(self):
        if self.hurdle_contact(self.food_cords):
            self.player.gotFood = True
            self.food_exists = False
            self.player.characterDefault = self.player.winDefault
            self.player.left = self.player.right = self.player.up = self.player.down = False

    def collision(self):
        self.wall_logic()
        self.hurdle_logic()
        self.food_logic()

    def have_won(self):
        self.show()
        self.message(msg="Yeah.!", x=self.gameDimension[0] // 2 - 50, y=self.gameDimension[1] // 2,
                     color=(110, 220, 40), font_size=30)
        pygame.display.flip()

    def have_died(self):
        pass


    def start_game(self):
        self.pause_game()

        while self.player.alive and not self.player.gotFood:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        self.player.left = True
                        self.player.right = self.player.up = self.player.down = False

                    if event.key == pygame.K_RIGHT:
                        self.player.right = True
                        self.player.left = self.player.up = self.player.down = False

                    if event.key == pygame.K_UP:
                        self.player.up = True
                        self.player.right = self.player.left = self.player.down = False

                    if event.key == pygame.K_DOWN:
                        self.player.down = True
                        self.player.right = self.player.up = self.player.left = False

                    if event.key == pygame.K_p:
                        self.pause_game()

            self.show()
            self.dynamics()
            self.collision()
            pygame.display.flip()
            if self.screen_capt:
                self.read_screen(stream=self.stream, gray=self.gray, maxi=self.maxi, store=self.store,
                                 player=self.player, vision_limit=50)
            self.clock.tick(30)
        if self.player.alive and self.player.gotFood:
            self.have_won()
        pygame.time.wait(2000)


if __name__ == "__main__":
    lvl = Level(None, (600, 350))
    lvl.start_game()
