import random
from time import sleep


# Identify which spell is being cast, by whom and who is being target.
def Spell(spell, caster, target):
    if spell == 'Fireball':
        fireball(caster, target)


def fireball(caster, target):
    mana_cost = 5
    base_dmg = 6
    hit_chance = 80
    caster.mana -= mana_cost
    print("{} casts Fireball!".format(caster.name))
    sleep(1.5)
    if random.randint(1, 100) < hit_chance:
        dmg_mod = base_dmg + random.randint(1, 6) * 2 - target.res['Fire'] + caster.mag / 2
        target.health -= dmg_mod
        print("Hit! {} dealt {} to {}".format(caster.name, dmg_mod, target.name))
    else:
        print("{} missed!".format(caster.name))
        sleep(1.0)

