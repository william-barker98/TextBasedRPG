from time import sleep


def CheckLevelRewards(p):  # party member
    # Hero
    if hasattr(p, 'allies'):
        if p.level == 2:
            p.spells['Heal'] = 3
            print("---> {} learned Heal! <---".format(p.name))
            sleep(1.5)
    if p.name == "Edgar":
        if p.level == 2:
            p.spells['Hasten'] = 6
            print("---> {} learned Hasten! <---".format(p.name))
            sleep(1.5)
    return
