from settings import *
from time import sleep
import random


def a_getCost(ability):
    if ability == "Rend":
        return 8
    if ability == "Ratchet Man":
        return 12
    pass


def a_getTargetType(ability):
    if ability == "Rend":
        return True
    if ability == "Ratchet Man":
        return True


def a_getDuration(ability):
    if ability == "Rend":
        return 3
    pass


def a_getWeapon(ability):
    if ability == "Rend":
        return "Axe"
    if ability == "Ratchet Man":
        return "Axe"


def Ability(ability, caster, target):
    if ability == "Rend":
        Rend(caster, target)
    if ability == "Ratchet Man":
        Ratchet_Man(caster, target)
    pass


def Rend(caster, target):
    caster.mana -= a_getCost('Rend')
    rend_chance = 65
    print("{}{}{} attacks {}{}{} with  {}Rend{} !"
          .format(caster.colour, caster.name, RESET, target.colour, target.name, RESET, ABILITIES_COLOUR, RESET))
    sleep(1.5)

    dmg_mod = round(caster.atk * 1.1) - target.defense
    target.health -= dmg_mod
    print(
        "Hit! {}{}{} dealt {}{}{} to {}{}".format(caster.colour, caster.name, RESET, DAMAGE_COLOUR, dmg_mod, RESET,
                                                  target.colour, target.name) + RESET)

    rended = random.randint(1, 101)
    if rended <= rend_chance:
        target.debuffs['Rend'] = a_getDuration('Rend')
        print("{}{}'s{} defense decreased!".format(target.colour, target.name, RESET))
        print("Target Defense OLD: {}".format(target.defense))
        target.defense -= target.defense // 2
        print("Target Defense NEW: {}".format(target.defense))


def Ratchet_Man(caster, target):
    caster.mana -= a_getCost('Ratchet Man')
    hit_chance = 25
    print("{}{}{} attacks {}{}{} with  {}Ratchet Man{} !"
          .format(caster.colour, caster.name, RESET, target.colour, target.name, RESET, ABILITIES_COLOUR, RESET))
    sleep(1.5)

    hit = random.randint(1, 101)
    if hit <= hit_chance:
        dmg_mod = random.randint(1, 6)
        dmg_dealt = caster.atk + dmg_mod
        if dmg_dealt < 1:
            dmg_dealt = 1
        target.health -= dmg_mod
        print(
            "Hit! {}{}{} dealt {}{}{} to {}{}".format(caster.colour, caster.name, RESET, DAMAGE_COLOUR, dmg_mod, RESET,
                                                      target.colour, target.name) + RESET)
