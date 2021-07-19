import random
from enemies import *
from time import sleep
import math
from playsound import playsound



class Player:
    def __init__(self, game):
        self.game = game
        self.max_health = 30
        self.health = 30
        self.mana = 10
        self.exp = 0
        self.gold = 0
        self.fighting = False
        self.atk = 13
        self.defense = 13
        self.agl = 13
        self.level = 1
        self.level_threshold = 30
        self.equipment = []
        self.inventory = []

    def levelUp(self):
        self.base_exp = 30
        self.exponent = 1.5
        self.level += 2
        self.max_health += 5
        self.health = self.max_health
        self.atk += 2
        self._def += 2
        self.agl += 2
        self.level_threshold = math.floor(self.base_exp * (self.level ** self.exponent))
        print("YOU HAVE LEVELLED UP!")
        playsound('Sounds/level_up.mp3')
        sleep(0.75)
        print("LVL: {}".format(self.level))
        print("ATK: +2")
        print("DEF: +2")
        print("AGL: +2")
        sleep(2.0)


    def action(self):

        print("What do you do?")
        choice = input("Fight[Z], Inventory[X], SHOP[C], SAVE[S], QUIT[Q]\n")
        if choice == "z" or choice == "Z":
            self.encounter()
        if choice == "x" or choice == "X":
            self.show_inventory()

    def encounter(self):
        enemy_types = ["Goblin", "Wolf"]
        flee_failed = False
        enemies = []
        defeated_mobs = []
        self.fighting = True
        spawn_count = random.randrange(1, 4)
        for enemy in range(spawn_count):
            type = random.choice(enemy_types)
            spawn = Enemies(type, self.game, self)
            enemies.append(spawn)
        for e in range(len(enemies)):
            print("You have encounterd a", enemies[e].type)
            sleep(0.5)

        while self.health > 0 and len(enemies) > 0:
            print("----------------------")
            print("----------------------")
            print("HP: {}/{}".format(self.health, self.max_health))
            for e in range(len(enemies)):
                if len(enemies) == 1:
                    print("Enemy", e + 1, ":", enemies[e].type, end="")
                else:
                    print("Enemy", e + 1, ":", enemies[e].type, ", ", end="")
            print("\nWhat would you like to do?\n")
            action = input("Attack: [Z], STATS: [X], Flee: [C]\n")
            print("----------------------\n")
            if action == "z" or action == "Z":
                print("[ATTACK]")
                self.attack(enemies, defeated_mobs)
            elif action == "c" or action == "C":
                if not flee_failed:
                    flee_failed = self.flee(enemies)
                else:
                    print("You cannot flee this encounter!")
                    sleep(1.5)
            elif action == "x" or action == "X":
                self.check_stats(enemies)
            else:
                print("INVALID INPUT")
                sleep(2.0)
        if self.health <= 0:
            print("YOU DIED")
        if len(enemies) == 0:
            self.fighting = False
            if len(defeated_mobs) < spawn_count:
                pass
            else:
                print("You have slain the enemy!")
                sleep(1.5)
                exp_gained = 0
                gold_gained = 0

                drops = []
                for e in range(len(defeated_mobs)):
                    self.exp += defeated_mobs[e].exp
                    exp_gained += defeated_mobs[e].gold
                    self.gold += defeated_mobs[e].gold
                    gold_gained += defeated_mobs[e].gold

                    drop_chance = defeated_mobs[e].drop_chance
                    if random.randint(1, 100) <= drop_chance:
                        drop = random.choice(defeated_mobs[e].drop_items)
                        self.inventory.append(drop)
                        print("You received a {}!".format(drop))




                print("You have gained {} exp!".format(exp_gained))
                print("EXP:", self.exp)
                print("You have gained {} gold!".format(gold_gained))
                print("GOLD:", self.gold)
                sleep(1.5)
                if self.exp >= self.level_threshold:
                    self.levelUp()

            print("----------------------")
            print("----------------------")

    def attack(self, enemies, defeated_mobs):
        if len(enemies) > 1:
            print("Which enemy will you attack?\n")
            for e in range(len(enemies)):
                if e + 1 == len(enemies):
                    print(enemies[e].type, e + 1, "[{}/{}]".format(enemies[e].health, enemies[e].max_health))
                else:
                    print(enemies[e].type, e + 1, "[{}/{}]".format(enemies[e].health, enemies[e].max_health), ", ", end="")
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
                sleep(1.5)
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
            print("The '{}' died.".format(enemies[choice].type))
            defeated_mobs.append(enemies[choice])
            enemies.remove(enemies[choice])

            print("----------------------")
        for e in enemies:
            e.action(self)

    def flee(self, enemies):
        highest_agl = 0
        print("You attempt to flee!")
        sleep(1.5)
        for e in range(len(enemies)):
            if enemies[e].agl > highest_agl:
                highest_agl = enemies[e].agl
        print("Highest AGL:", highest_agl)
        flee_mod = random.randint(1, 6)
        flee_result = self.agl + flee_mod
        if flee_result > highest_agl:
            print("You fled...")
            enemies.clear()
            sleep(1.5)

        else:
            print("You failed to flee!")
            return True

    def check_stats(self, enemies):
        for e in range(len(enemies)):
            print((e + 1), ":", enemies[e].type)
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