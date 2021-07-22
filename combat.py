import operator
from time import sleep
from settings import *
from colorama import Fore

from enemies import *
#from player import Player



def Combat(hero):
    global enemies
    global defeated_mobs
    global flee_failed
    global spawn_count
    global ended
    global turn_order
    global spawn_count
    turn_order = []
    spawn_result = []
    enemies = []
    defeated_mobs = []
    spawn_count = 0

    ended = False
    Setup(hero)


def Setup(hero):
    # Spawn Enemies
    enemy_types = ["Goblin", "Wolf"]
    spawn_count = random.randrange(1, 4)
    spawn_names = []
    dups = {}   # Stores name duplicates

    for spawn in range(spawn_count):
        name = random.choice(enemy_types)
        spawn = Enemies(name)
        spawn_names.append(spawn.name)
        enemies.append(spawn)
        print("You have encounterd a", spawn.name)
        sleep(0.5)

    for i, val in enumerate(spawn_names):
        if val not in dups:
            # Store index of first occurrence and occurrence value
            dups[val] = [i, 1]
        else:
            # Special case for first occurrence
            if dups[val][1] == 1:
                spawn_names[dups[val][0]] += " " + str(dups[val][1])

            # Increment occurrence value, index value doesn't matter anymore
            dups[val][1] += 1

            # Use stored occurrence value
            spawn_names[i] += " " + str(dups[val][1])
    print(spawn_names)
    i = 0
    for e in enemies:
        e.name = spawn_names[i]
        i += 1













    Initiative(hero)




def Initiative(hero):
    while hero.health > 0 and len(enemies) > 0:
        # Initiative Rolls
        turn_order = []
        # Hero Initiative
        init_mod = random.randint(1, 6)
        hero.initiative = hero.agl + init_mod
        turn_order.append(hero)
        # Ally Initiative
        for a in hero.allies:
            if a.dead is True:
                pass
            else:
                init_mod = random.randint(1, 6)
                a.initiative = a.agl + init_mod
                turn_order.append(a)

        # Enemy Initiative
        for e in enemies:
            if e.dead is True:
                pass
            else:
                init_mod = random.randint(1, 6)
                e.initiative = e.agl + init_mod
                turn_order.append(e)

        turn_order.sort(key=operator.attrgetter('initiative'))
        turn_order.reverse()

        if not ended:
            for char in turn_order:
                Turn(char, hero)
                if ended:
                    break


def Turn(char, hero):
    if not ended:
        if char.health <= 0:
            if char.dead is True:
                pass
            else:
                print("{} died.".format(char.name))
                char.dead = True

            pass
        else:
            print("----------------------")
            print(char.colour + "{}: HP:[{}/{}] MP:[{}/{}]".format(char.name.upper(), char.health, char.max_health, char.mana, char.max_mana))
            print("----------------------")
            sleep(2.5)
            if isinstance(char, Enemies):
                char.action(hero)

            else:
                char.action(enemies, defeated_mobs)
            sleep(2.0)
            print("\n")
        Check_Outcome(hero, char, enemies)


def Check_Outcome(hero, char, enemies):
    # Check if all enemies are dead.

    if len(enemies) == 0:
        ended = Victory(hero)


def Victory(hero):
    exp_gained = 0
    gold_gained = 0
    party = []
    party.append(hero)
    for a in hero.allies:
        party.append(a)

    drops = []
    for p in party:
        if p == hero:
            for e in range(len(defeated_mobs)):
                hero.gold += defeated_mobs[e].gold
                gold_gained += defeated_mobs[e].gold
                exp_gained += defeated_mobs[e].exp
                drop_chance = defeated_mobs[e].drop_chance
                if random.randint(1, 100) <= drop_chance:
                    drop = random.choice(defeated_mobs[e].drop_items)
                    hero.inventory.append(drop)
                    print("You received a {}{}{}!".format(DROP_COLOUR, drop, Fore.RESET))


    for p in party:
        if p.dead is False:
            p.exp += exp_gained
        else:
            pass
    pass

    print("You have gained {} exp!".format(exp_gained))
    print("EXP: +{}".format(exp_gained), )
    print("You have gained {} gold!".format(gold_gained))
    print("GOLD: +{} ".format(gold_gained))
    sleep(1.5)

    for p in party:
        if p.exp >= p.level_threshold:
            p.levelUp()

    print("----------------------\n")
    global ended
    ended = True

