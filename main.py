import random
import sys
from player import *
from time import sleep
from enemies import *


class Game:
    def __init__(self):
        self.running = True


    def run(self):
        print("Welcome to RPG!\n")
        print("---------------\n")
        while self.running:
            player.action()
            if not player.fighting:
                player.action()
            pass
        else:
            sys.exit()

base_exp = 30
exponent = 1.5
level = 1
for i in range(20):
    print("Level", level, ":", math.floor(base_exp * (level ** exponent)))
    level += 1



game = Game()
player = Player(game)
game.run()
