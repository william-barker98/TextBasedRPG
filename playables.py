import math
import time
from settings import *

from colorama import Fore, Back
from colorama import init

from combat import Combat
from skills import *
from sounds import PlaySound
from spells import *
from abilities import *

init(autoreset=True)
global flee_failed
print(Back.BLACK)


class Player:
    def __init__(self, game, name: object):
        self.name = name
        self.game = game
        self.max_health = 30
        self.health = 30
        self.max_mana = 10
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
        self.spells = ['Haste']
        self.abilities = []
        self.equipment = {}
        self.inventory = []
        self.allies = []
        self.initiative = 0
        self.dead = False
        self.getParty()
        self.colour = Fore.LIGHTCYAN_EX
        self.buffs = {}
        self.debuffs = {}
        self.skill_points = 0
        self.skills = {'Swords': 0, 'Spears': 0, 'Shields': 0}

    def getParty(self):
        edgar = Ally("Edgar")
        self.allies.append(edgar)
        # katie = Ally("Katie")
        # self.allies.append(katie)
        # yorkshire = Ally("Yorkshire")
        # self.allies.append(yorkshire)
        global party
        party = [self]
        for a in self.allies:
            party.append(a)

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
        self.max_mana += 5
        self.mana = self.max_mana
        self.skill_points += 5
        self.level_threshold = math.floor(self.base_exp * (self.level ** self.exponent))
        print("{}{}{} HAS LEVELLED UP!".format(self.colour, self.name, RESET))
        PlaySound('Sounds/level_up.mp3', 0.2)
        time.sleep(3)
        print("LVL: {}".format(self.level))
        print("HP: +5")
        print("MP: +5")
        print("ATK: +2")
        print("DEF: +2")
        print("AGL: +2")
        print("MAG: +2")
        time.sleep(2.0)

        CheckLevelRewards(self)
        print("{}{}{} has gained {}{}{} skill points!".format(self.colour, self.name, RESET, DAMAGE_COLOUR, "5", RESET))
        sleep(1.0)
        allocate = input("Allocate points now?: [Y]/[N]")

        while allocate is not "Y" or allocate is not "N":
            print("WRONG INPUT. TRY AGAIN")

        if allocate == "Y":
            AllocateSkillPoints(self, self.skill_points + 5)
        elif allocate == "N":
            pass



    def activity(self):
        print(self.buffs.items(), "\n")
        print("What do you do?")
        choice = input("""
Fight[Z]
Inventory[X]
STATS[C]
SHOP[V]
SAVE[S]
QUIT[Q]\n""")

        if choice == "z" or choice == "Z":
            Combat(self)
        if choice == "x" or choice == "X":
            self.show_inventory()
        if choice == "c" or choice == "C":
            self.show_team()

    def action(self, enemies, defeated_mobs):
        flee_failed = False

        i = 0
        for e in enemies:
            print(Fore.LIGHTRED_EX + "[{}]: {}: HP:[{}/{}] MP[{}/{}]".format(i + 1, e.name, e.health, e.max_health,
                                                                             e.mana, e.max_mana))
            i += 1
            if i == len(enemies):
                print("")
        for p in party:
            print(self.colour + "{}: HP:[{}/{}] MP[{}/{}]".format(p.name, p.health, p.max_health, p.mana, p.max_mana))
        print("\nWhat would you like to do?\n")
        print("----------------------")
        action = input("Attack: [Z], Abilities: [X], Spells: [C], Flee: [V]\n")

        if action == "z" or action == "Z":
            print("[ATTACK]")
            self.attack(enemies, defeated_mobs)

        elif action == "x" or action == "X":
            self.ability(enemies, defeated_mobs)
            pass

        elif action == "c" or action == "C":
            self.spell(enemies, defeated_mobs)

        elif action == "v" or action == "V":
            if not flee_failed:
                print("[FLEE]")
                flee_failed = self.flee(enemies)
            else:
                print("You cannot flee this encounter!")
                time.sleep(1.5)

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
            i = 0
            for e in enemies:
                print(Fore.LIGHTRED_EX + "[{}]: {}: HP:[{}/{}] MP[{}/{}]".format(i + 1, e.name, e.health, e.max_health,
                                                                                 e.mana, e.max_mana) + RESET)
                i += 1
                if i == len(enemies):
                    print("")

            choice = input()
            if choice.isdigit():
                choice = int(choice)
            else:
                print("Illegal Input. Try again.")
                self.attack(enemies, defeated_mobs)
                return
            if choice > len(enemies) or choice <= 0:
                print("ENEMY DOES NOT EXIST")
                time.sleep(1.5)
                self.attack(enemies, defeated_mobs)
                return
            choice -= 1

        else:
            choice = 0

        # the attack calculation
        target = enemies[choice]
        dmg_mod = random.randint(1, 6)
        dmg_dealt = self.atk + dmg_mod - target.defense
        if dmg_dealt < 1:
            dmg_dealt = 1
        print("{}{}{} attacks the {}{}{} for {}{}{} damage!".format(self.colour, self.name, RESET, target.colour,
                                                                    target.name, RESET, DAMAGE_COLOUR, dmg_dealt,
                                                                    RESET))
        target.health -= dmg_dealt
        if target.health < 1:
            self.kill_enemy(target, enemies, defeated_mobs)

    def ability(self, enemies, defeated_mobs):
        print("[ABILITIES]")
        i = 0
        if 0 == len(self.abilities):
            print("{}{}{} has not learned any {}abilities{}."
                  .format(self.colour, self.name, RESET, ABILITIES_COLOUR, RESET))
            sleep(2.0)
            print("------------------------------")
            self.action(enemies, defeated_mobs)
            return
        for ability in self.abilities:
            print("{}[{}]: {}: {}".format(ABILITIES_COLOUR, i + 1, ability, a_getCost(ability)) + RESET)
            i += 1
        print("")
        choice_ability = input("Cast a spell ([B] to back).")

        if choice_ability.isdigit():
            choice_ability = int(choice_ability)
        else:
            print("Illegal Input. Try again.")
            self.ability(enemies, defeated_mobs)
            return
        if choice_ability > len(self.abilities) or choice_ability <= 0:
            print("ABILITY DOES NOT EXIST")
            time.sleep(1.5)
            self.ability(enemies, defeated_mobs)
            return
            # -1 so choice_spell can be used as an index.
        choice_ability -= 1

        ability_type = a_getType(self.abilities[choice_ability])
        print("TYPE: ", ability_type)

        # If ability is offensive (targets enemies):
        if ability_type:
            for e in range(len(enemies)):
                print("{}[{}]: {}: HP[{}/{}] MP[{}/{}]".format(enemies[e].colour, e + 1, enemies[e].name,
                                                               enemies[e].health, enemies[e].max_health,
                                                               enemies[e].mana, enemies[e].max_mana) + RESET)

            choice = input()
            if choice.isdigit():
                choice = int(choice)
            else:
                print("Illegal Input. Try again.")
                self.ability(enemies, defeated_mobs)
            if choice > len(enemies) or choice <= 0:
                print("ENEMY DOES NOT EXIST")
                time.sleep(1.5)
                self.ability(enemies, defeated_mobs)
                return
            choice -= 1
            target = enemies[choice]

        # If spell is friendly (targets allies):
        elif not ability_type:
            i = 0
            for p in party:
                print(
                    self.colour + "[{}]: {}: HP:[{}/{}] MP[{}/{}]".format(i + 1, p.name, p.health, p.max_health, p.mana,
                                                                          p.max_mana))
                i += 1

            choice = input("Cast a spell ([B] to back).")
            if choice.isdigit():
                choice = int(choice)
            choice -= 1
            target = party[choice]
        if a_getCost(self.abilities[choice_ability]) > self.mana:
            print("Not enough mana.")
            self.ability(enemies, defeated_mobs)
            return
        Ability(self.abilities[choice_ability], self, target)
        if ability_type is True:
            if target.health <= 0:
                self.kill_enemy(target, enemies, defeated_mobs)



    def spell(self, enemies, defeated_mobs):
        print("[SPELLS]")
        i = 0
        if 0 == len(self.spells):
            print("{} has not learned any spells.".format(self.name))
            sleep(2.0)
            print("------------------------------")
            self.action(enemies, defeated_mobs)
            return
        for spell in self.spells:
            print("{}[{}]: {}: {}".format(SPELL_COLOUR, i + 1, spell, s_getCost(spell)) + RESET)
            i += 1
        print("")
        choice_spell = input("Cast a spell ([B] to back).")
        if choice_spell.isdigit():
            choice_spell = int(choice_spell)
        else:
            print("Illegal Input. Try again.")
            self.spell(enemies, defeated_mobs)
            return
        if choice_spell > len(self.spells) or choice_spell <= 0:
            print("SPELL DOES NOT EXIST")
            time.sleep(1.5)
            self.spell(enemies, defeated_mobs)
            return
        # -1 so choice_spell can be used as an index.
        choice_spell -= 1

        spell_type = s_getType(self.spells[choice_spell])
        print("TYPE: ", spell_type)

        # If spell is offensive:
        if spell_type:
            for e in range(len(enemies)):
                print("{}[{}]: {}: HP[{}/{}] MP[{}/{}]".format(enemies[e].colour, e + 1, enemies[e].name,
                                                               enemies[e].health, enemies[e].max_health,
                                                               enemies[e].mana, enemies[e].max_mana) + RESET)

            choice = input()
            if choice.isdigit():
                choice = int(choice)
            else:
                print("Illegal Input. Try again.")
                self.spell(enemies, defeated_mobs)
            if choice > len(enemies) or choice <= 0:
                print("ENEMY DOES NOT EXIST")
                time.sleep(1.5)
                self.spell(enemies, defeated_mobs)
                return
            choice -= 1
            target = enemies[choice]

        # If spell is friendly:
        elif not spell_type:
            i = 0
            for p in party:
                print(
                    self.colour + "[{}]: {}: HP:[{}/{}] MP[{}/{}]".format(i + 1, p.name, p.health, p.max_health, p.mana,
                                                                          p.max_mana))
                i += 1

            choice = input("Cast a spell ([B] to back).")
            if choice.isdigit():
                choice = int(choice)
            choice -= 1
            target = party[choice]
        if s_getCost(self.spells[choice_spell]) > self.mana:
            print("Not enough mana.")
            self.spell(enemies, defeated_mobs)
            return
        Spell(self.spells[choice_spell], self, target)
        if spell_type is True:
            if target.health <= 0:
                self.kill_enemy(target, enemies, defeated_mobs)

    def kill_enemy(self, target, enemies, defeated_mobs):
        print("'{}{}{}' died.".format(target.colour, target.name, RESET))
        time.sleep(1.5)
        target.dead = True
        defeated_mobs.append(target)
        enemies.remove(target)
        return

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
        for p in party:
            print("----------------------")
            print(p.name.upper())
            print("----------------------")
            print("     LVL:", p.level)
            print("     HP: {}/{}".format(p.health, p.max_health))
            print("     MP: {}/{}".format(p.mana, p.max_mana))
            print("     ATK:", p.atk)
            print("     DEF:", p.defense)
            print("     AGL", p.agl)


class Ally(Player):
    def __init__(self, name):
        self.name = name
        self.dead = False
        self.colour = Fore.LIGHTCYAN_EX
        self.buffs = {}
        self.debuffs = {}
        self.res = {'Fire': 5, 'Shock': 5}
        self.skill_points = 0
        if name == "Edgar":
            self.max_health = 28
            self.health = 28
            self.max_mana = 12
            self.mana = 12
            self.exp = 0
            self.atk = 15
            self.defense = 9
            self.agl = 9
            self.mag = 12
            self.level = 1
            self.level_threshold = 30
            self.spells = []
            self.abilities = ['Rend']
            self.equipment = []
            self.initiative = 0

        if name == "Katie":
            self.max_health = 22
            self.health = 22
            self.max_mana = 20
            self.mana = 20
            self.exp = 0
            self.atk = 11
            self.defense = 11
            self.agl = 25
            self.mag = 16
            self.level = 1
            self.level_threshold = 30
            self.spells = ['Fireball', 'Heal']
            self.abilities = []
            self.equipment = []
            self.initiative = 0

        if name == "Yorkshire":
            self.max_health = 30
            self.health = 30
            self.max_mana = 6
            self.mana = 6
            self.exp = 0
            self.atk = 13
            self.defense = 13
            self.agl = 13
            self.mag = 5
            self.level = 1
            self.level_threshold = 30
            self.spells = ['Haste']
            self.abilities = []
            self.equipment = []

        self.base_atk = self.atk
        self.base_def = self.defense
        self.base_agl = self.agl
        self.base_mag = self.mag
        self.base_res = self.res
        self.initiative = 0
