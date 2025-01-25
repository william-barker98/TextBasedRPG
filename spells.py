import random
from time import sleep
from settings import *
from colorama import Fore


def s_getCost(spell):
    if spell == "Fireball":
        return 4
    if spell == "Heal":
        return 3
    if spell == "Haste":
        return 6
    if spell == "Sizz":
        return 8

# Returns the value of a spell (dmg, heal, buff, debuff etc).


def s_getTargetType(spell):
    if spell == "Fireball":
        return True
    if spell == "Heal":
        return False
    if spell == "Haste":
        return False
    if spell == "Sizz":
        return True



def s_getMultiTarget(spell):
    if spell == "Sizz":
        return True
    else:
        return False



def s_getDuration(spell):
    if spell == 'Haste':
        return 3
    else:
        return False


# Identify which spell is being cast, by whom and who is being target.
def Spell(spell, caster, target):
    caster.mana -= s_getCost(spell)
    if spell == 'Fireball':
        fireball(caster, target)
    elif spell == 'Heal':
        heal(caster, target)
    elif spell == 'Haste':
        haste(caster, target)
    elif spell == 'Sizz':
        sizz(caster, target)


def fireball(caster, target):
    base_dmg = 4
    hit_chance = 80
    #caster.mana -= s_getCost('Fireball')
    print("{} casts {}Fireball{}!".format(caster.name, SPELL_COLOUR, RESET))
    sleep(1.5)
    if random.randint(1, 101) <= hit_chance:
        dmg_mod = base_dmg + random.randint(1, 6) * 2 - target.res['Fire'] + caster.mag // 2
        target.health -= dmg_mod
        print(
            "Hit! {}{}{} dealt {}{}{} to {}{}".format(caster.colour, caster.name, RESET, DAMAGE_COLOUR, dmg_mod, RESET,
                                                      target.colour, target.name) + RESET)
    else:
        print("{} missed!".format(caster.name))
        sleep(1.0)


def sizz(caster, target):
    #caster.mana -= s_getCost('Sizz')
    base_dmg = 4
    hit_chance = 99
    print("{} casts {}Sizz{}!".format(caster.name, SPELL_COLOUR, RESET))
    for t in target:
        sleep(1.5)
        if random.randint(1, 101) <= hit_chance:
            dmg_mod = base_dmg + random.randint(1, 6) * 2 - t.res['Fire'] + caster.mag // 2
            t.health -= dmg_mod
            print(
                "Hit! {}{}{} dealt {}{}{} to {}{}".format(caster.colour, caster.name, RESET, DAMAGE_COLOUR, dmg_mod,
                                                          RESET,
                                                          t.colour, t.name) + RESET)
        else:
            print("{} missed!".format(caster.name))
            sleep(1.0)






def heal(caster, target):
    heal_amount = 30
    print("{}{}{} casts {}Heal{} on {}{}{}!".format(caster.colour, caster.name, RESET, SPELL_COLOUR_HEAL, RESET,
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
    print(
        "{}{}{} casts {}Haste{} on {}{}{}".format(caster.colour, caster.name, RESET, SPELL_COLOUR, RESET, target.colour,
                                                  target.name, RESET))
    target.buffs['Haste'] = s_getDuration('Haste')
    print("{}{}'s{} agility increased!".format(target.colour, target.name, RESET))
    target.agl += 5
