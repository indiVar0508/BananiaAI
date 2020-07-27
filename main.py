from Level.level_one import Level
from Character.capo import CAPO


class Main:

    def __init__(self):
        self.player = CAPO(step=10, draw=False, x=30, y=200, length=30, width=30, color=(230, 220, 50))
        dim = (700, 400)
        self.level = Level(self.player, game_dimension=dim, screen_capt=False, stream=True,
                           gray=False, maxi=False, store=False)

    def start(self):
        self.level.start_game()


if __name__ == "__main__":
    main = Main()
    main.start()
