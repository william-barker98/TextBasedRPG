import random
from time import sleep


def getCost(spell):
    if spell == "Fireball":
        return 5


def getType(spell):
    if spell == "Fireball":
        return True
    if spell == "Heal":
        return False
    if spell == "Hasten":
        return False


# Identify which spell is being cast, by whom and who is being target.
def Spell(spell, caster, target):
    if spell == 'Fireball':
        fireball(caster, target)
    elif spell == 'Heal':
        heal(caster, target)
    elif spell == 'Hasten':
        hasten(caster, target)


def fireball(caster, target):
    mana_cost = 5
    base_dmg = 4
    hit_chance = 80
    caster.mana -= mana_cost
    print("{} casts Fireball!".format(caster.name))
    sleep(1.5)
    if random.randint(1, 100) <= hit_chance:
        dmg_mod = base_dmg + random.randint(1, 6) * 2 - target.res['Fire'] + caster.mag // 2
        target.health -= dmg_mod
        print("Hit! {} dealt {} to {}".format(caster.name, dmg_mod, target.name))
    else:
        print("{} missed!".format(caster.name))
        sleep(1.0)


def heal(caster, target):
    heal_amount = 30
    print("{} casts Heal on {}!".format(caster.name, target.name))
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

def hasten(caster, target):
    target.agl += 5