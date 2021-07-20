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
        edgar = Ally("Edgar", )
        katie = Ally("Katie", )
        yorkshire = Ally("Yorkshire", )
        hero.allies.append(edgar)
        hero.allies.append(katie)
        hero.allies.append(yorkshire)
        while self.running:
            hero.activity()
        else:
            sys.exit()


game = Game()

game.run()
