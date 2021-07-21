from playables import *
import sys


class Game:
    def __init__(self):
        self.running = True

    def run(self):
        print("Welcome to RPG!\n")
        print("---------------\n")
        hero_name = input("Please enter your name:\n")
        hero = Player(game, hero_name)
        while self.running:
            hero.activity()
        else:
            sys.exit()


game = Game()
game.run()
