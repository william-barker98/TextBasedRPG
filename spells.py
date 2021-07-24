import random
from time import sleep
from settings import *
from colorama import Fore


def getCost(spell):
    if spell == "Fireball":
        return 5
    if spell == "Heal":
        return 3
    if spell == "Haste":
        return 6


# Returns the value of a spell (dmg, heal, buff, debuff etc).
def getValue():
    pass


def getType(spell):
    if spell == "Fireball":
        return True
    if spell == "Heal":
        return False
    if spell == "Haste":
        return False


def getDuration(spell):
    if spell == 'Haste':
        return 2
    else:
        return False


# Identify which spell is being cast, by whom and who is being target.
def Spell(spell, caster, target):
    if spell == 'Fireball':
        fireball(caster, target)
    elif spell == 'Heal':
        heal(caster, target)
    elif spell == 'Haste':
        haste(caster, target)


def fireball(caster, target):
    mana_cost = 5
    base_dmg = 4
    hit_chance = 80
    caster.mana -= mana_cost
    print("{} casts {}Fireball{}!".format(caster.name, SPELL_COLOUR_OFF, RESET))
    sleep(1.5)
    if random.randint(1, 100) <= hit_chance:
        dmg_mod = base_dmg + random.randint(1, 6) * 2 - target.res['Fire'] + caster.mag // 2
        target.health -= dmg_mod
        print(
            "Hit! {}{}{} dealt {}{}{} to {}{}".format(caster.colour, caster.name, RESET, DAMAGE_COLOUR, dmg_mod, RESET,
                                                      target.colour, target.name) + RESET)
    else:
        print("{} missed!".format(caster.name))
        sleep(1.0)


def heal(caster, target):
    heal_amount = 30
    print("{}{}{} casts {}Heal{} on {}{}{}!".format(caster.colour, caster.name, RESET, SPELL_COLOUR_DEF, RESET,
                                                    target.colour, target.name, RESET))
    sleep(1.5)
    diff = target.max_health - target.health
    if target.health == target.max_health:
        print("{} is already at max health!".format(target.name))
        return
    if diff < heal_amount:
        target.health += diff
        print("{} is healed for {}".format(target.name, diff))
    else:
        target.health += heal_amount
        print("{} is healed for {}".format(target.name, heal_amount))


def haste(caster, target):
    target.buffs['Haste'] = getDuration('Haste')
    target.agl += 5
