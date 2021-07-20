import math
import time
import random
from combat import Combat
from spells import Spell

global flee_failed
from playsound import playsound


class Player:
    def __init__(self, game, name: object):
        self.name = name
        self.game = game
        self.max_health = 30
        self.health = 30
        self.mana = 10
        self.exp = 0
        self.gold = 0
        self.atk = 13
        self.defense = 13
        self.agl = 25
        self.mag = 10
        self.res = {'Fire': 5, 'Shock': 5}
        self.level = 1
        self.level_threshold = 30
        self.spells = ['Heal']
        self.abilities = []
        self.equipment = []
        self.inventory = []
        self.allies = []
        self.initiative = 0
        self.dead = False


    def levelUp(self):
        self.base_exp = 30
        self.exponent = 1.5
        self.level += 1
        self.max_health += 5
        self.health = self.max_health
        self.atk += 2
        self.defense += 2
        self.agl += 2
        self.mag += 2
        self.mana += 5
        self.level_threshold = math.floor(self.base_exp * (self.level ** self.exponent))
        print("{} HAS LEVELLED UP!".format(self.name))
        playsound('Sounds/level_up.mp3')
        time.sleep(0.75)
        print("LVL: {}".format(self.level))
        print("HP: +5")
        print("MP: +5")
        print("ATK: +2")
        print("DEF: +2")
        print("AGL: +2")
        print("MAG: +2")


        time.sleep(2.0)

    def activity(self):
        print("What do you do?")
        choice = input("Fight[Z], Inventory[X], STATS[C], SHOP[V], SAVE[S], QUIT[Q]\n")
        if choice == "z" or choice == "Z":
            Combat(self)
        if choice == "x" or choice == "X":
            self.show_inventory()
        if choice == "c" or choice == "C":
            self.show_team()

    def action(self, enemies, defeated_mobs):
        flee_failed = False
        print("HP: {}/{}".format(self.health, self.max_health))
        for e in range(len(enemies)):
            if len(enemies) == 1:
                print("Enemy", e + 1, ":", enemies[e].name, "[{}/{}]".format(enemies[e].health, enemies[e].max_health), end="")
            else:
                print("Enemy", e + 1, ":", enemies[e].name, "[{}/{}]".format(enemies[e].health, enemies[e].max_health), ", ", end="")
        print("\nWhat would you like to do?\n")
        action = input("Attack: [Z], STATS: [X], Flee: [C]\n")
        print("----------------------\n")
        if action == "z" or action == "Z":
            print("[ATTACK]")
            self.attack(enemies, defeated_mobs)
        elif action == "x" or action == "X":
            print("[SPELL]")
            Spell("Fireball", self, enemies[0])
            if enemies[0].health <= 0:
                kill_enemy(enemies[0])

        elif action == "c" or action == "C":
            if not flee_failed:
                print("[FLEE]")
                flee_failed = self.flee(enemies)
            else:
                print("You cannot flee this encounter!")
                time.sleep(1.5)

            self.check_stats(enemies)
            self.action(enemies, defeated_mobs)

        else:
            print("INVALID INPUT")
            time.sleep(1.0)
            self.action(enemies, defeated_mobs)

        if self.health <= 0:
            print("YOU DIED")
            pass
        else:
            pass

    def attack(self, enemies, defeated_mobs):
        if len(enemies) > 1:
            print("Which enemy will you attack?\n")
            for e in range(len(enemies)):
                if e + 1 == len(enemies):
                    print(enemies[e].name, e + 1, "[{}/{}]".format(enemies[e].health, enemies[e].max_health))
                else:
                    print(enemies[e].name, e + 1, "[{}/{}]".format(enemies[e].health, enemies[e].max_health), ", ", end="")
            for e in range(len(enemies)):
                if e + 1 == len(enemies):
                    print("[{}]".format(e + 1))
                else:
                    print("[{}]".format(e + 1), ", ", end="")
            choice = input()
            if choice.isdigit():
                choice = int(choice)
            else:
                choice = 1
            if choice > len(enemies) or choice <= 0:
                print("ENEMY DOES NOT EXIST")
                time.sleep(1.5)
                return
            choice -= 1

        else:
            choice = 0

        # the attack calculation
        dmg_mod = random.randint(1, 6)
        dmg_dealt = self.atk + dmg_mod - enemies[choice].defense
        if dmg_dealt < 1:
            dmg_dealt = 1
        print("ATK:", self.atk, ", D6:", dmg_mod, ", DEF:", enemies[choice].defense)
        print("Your attack does {} damage!".format(dmg_dealt))
        enemies[choice].health -= dmg_dealt
        if enemies[choice].health < 1:
            print("The '{}' died.".format(enemies[choice].name))
            time.sleep(1.5)
            enemies[choice].dead = True
            defeated_mobs.append(enemies[choice])
            enemies.remove(enemies[choice])
            print("Added Enemy")


    def flee(self, enemies):
        highest_agl = 0
        print("You attempt to flee!")
        time.sleep(1.5)
        for e in range(len(enemies)):
            if enemies[e].agl > highest_agl:
                highest_agl = enemies[e].agl
        print("Highest AGL:", highest_agl)
        flee_mod = random.randint(1, 6)
        flee_result = self.agl + flee_mod
        if flee_result > highest_agl:
            print("You fled...")
            enemies.clear()
            time.sleep(1.5)

        else:
            print("You failed to flee!")
            for e in enemies:
                e.action(self)
            return True

    def check_stats(self, enemies):
        for e in range(len(enemies)):
            print((e + 1), ":", enemies[e].name)
            print("----------------------")
            print("     LVL:", enemies[e].lvl)
            print("     HP: {}/{}".format(enemies[e].health, enemies[e].max_health))
            print("     ATK:", enemies[e].atk)
            print("     DEF:", enemies[e].defense)
            print("     AGL", enemies[e].agl)

    def show_inventory(self):
        print("INVENTORY")
        print("---------")
        for item in self.inventory:
            print("     {}".format(item))
        print("---------")

    def show_team(self):
        party = [self]
        for a in self.allies:
            party.append(a)
        for p in party:
            print("----------------------")
            print(p.name.upper())
            print("----------------------")
            print("     LVL:", p.level)
            print("     HP: {}/{}".format(p.health, p.max_health))
            print("     ATK:", p.atk)
            print("     DEF:", p.defense)
            print("     AGL", p.agl)


class Ally(Player):
    def __init__(self, name):
        self.name = name
        self.dead = False
        if name == "Edgar":
            self.max_health = 28
            self.health = 28
            self.mana = 12
            self.exp = 0
            self.atk = 13
            self.defense = 9
            self.agl = 9
            self.mag = 12
            self.level = 1
            self.level_threshold = 30
            self.spells = ['Hasten']
            self.abilities = []
            self.equipment = []
            self.initiative = 0

        if name == "Katie":
            self.max_health = 22
            self.health = 22
            self.mana = 14
            self.exp = 0
            self.atk = 11
            self.defense = 11
            self.agl = 16
            self.level = 1
            self.level_threshold = 30
            self.spells = ['Fireball']
            self.abilities = []
            self.equipment = []
            self.initiative = 0

        if name == "Yorkshire":
            self.max_health = 30
            self.health = 30
            self.mana = 10
            self.exp = 0
            self.atk = 13
            self.defense = 13
            self.agl = 13
            self.level = 1
            self.level_threshold = 30
            self.spells = []
            self.abilities = []
            self.equipment = []
            self.initiative = 0

