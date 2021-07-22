from time import sleep
from spells import getCost

def CheckLevelRewards(p):  # party member
    # Hero
    if hasattr(p, 'allies'):
        if p.level == 2:
            p.spells['Heal'] = getCost('Heal')
            print("---> {} learned Heal! <---".format(p.name))
            sleep(1.5)
    if p.name == "Edgar":
        if p.level == 2:
            p.spells['Hasten'] = getCost('Hasten')
            print("---> {} learned Hasten! <---".format(p.name))
            sleep(1.5)
    return
