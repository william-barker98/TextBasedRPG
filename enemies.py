import random
import colorama
from colorama import Fore
from settings import *


class Enemies:
    def __init__(self, name):
        self.name = name
        self.type = type
        self.initiative = 0
        self.dead = False
        self.colour = Fore.LIGHTRED_EX
        if "Goblin" in name:
            self.max_health = 13
            self.health = 13
            self.max_mana = 0
            self.mana = 0
            self.atk = 10
            self.defense = 10
            self.agl = 12
            self.gold = 5
            self.exp = 25
            self.lvl = 1
            self.drop_chance = 50
            self.drop_items = ["Medicinal Herb"]
            self.actions = ['ATTACK', 'IDLE']
            self.res = {'Fire': 4, 'Shock': 3}

        if "Wolf" in name:
            self.max_health = 12
            self.health = 12
            self.max_mana = 0
            self.mana = 0
            self.atk = 14
            self.defense = 10
            self.agl = 24
            self.gold = 2
            self.exp = 4
            self.lvl = 1
            self.drop_chance = 50
            self.drop_items = ["Medicinal Herb"]
            self.actions = ['ATTACK', 'CRIT']
            self.res = {'Fire': 1, 'Shock': 2}


    def action(self, player):
        if self.health <= 0:
            pass
        else:
            action = random.choice(self.actions)
            if action == "ATTACK":
                self.attack(False, player)
            if action == "CRIT":
                self.attack(True, player)
            if action == "IDLE":
                print(self.name, "is idle.")
                pass



    def attack(self, crit, player):
        # Select party member to attack
        targets = []
        if player.dead is False:
            targets = [player]
        else:
            pass
        for a in player.allies:
            if a.dead is False:
                targets.append(a)
            else:
                pass
        target = random.choice(targets)

        dmg_mod = random.randint(1, 6)
        dmg_dealt = self.atk + dmg_mod - target.defense
        if dmg_dealt < 1:
            dmg_dealt = 1
        target.health -= dmg_dealt
        print("{}{}{} attacks {}{}{} for {}{}{} damage!".format(self.colour, self.name, Fore.RESET, target.colour, target.name, Fore.RESET, DAMAGE_COLOUR, dmg_dealt, Fore.RESET))
        if target.health <= 0:
            if target.dead is True:
                pass

            print("{} has been slain :'(".format(target.name))
            target.dead = True
            targets.remove(target)


