from time import sleep
from spells import *

def CheckLevelRewards(p):  # party member
    # Hero
    if hasattr(p, 'allies'):
        if p.level == 2:
            p.spells.append('Heal')
            print("---> {} learned Heal! <---".format(p.name))
            sleep(1.5)
    if p.name == "Edgar":
        if p.level == 2:
            p.spells.append('Haste')
            print("---> {} learned Haste! <---".format(p.name))
            sleep(1.5)
    return

def AllocateSkillPoints(char, points):
    skills = char.skills.keys()
    values = char.skills.values()


    pass