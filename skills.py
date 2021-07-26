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


def CheckSkillRewards(char, skill):
    if hasattr(char, "allies"):
        if skill == "Swords":
            if char.skills["Swords"] >= 5 and "Rend" not in char.abilities:
                char.abilities.append("Rend")
                print("You have learned Rend!")

    pass


def AllocateSkillPoints(char, points):
    skills = list(char.skills)
    values = char.skills.values()
    i = 1
    for skill, value in char.skills.items():
        print("[{}]: {}: {}".format(i, skill, value))
        i += 1

    choice_skill = input("Select a skill ([B] to back.")
    while not choice_skill.isdigit():
        print("WRONG")
    choice_skill = int(choice_skill)
    choice_skill -= 1

    print("----------")
    print(skills[choice_skill])
    print("----------")

    choice_allocate = input("How many would you like to allocate?")
    while not choice_allocate.isdigit():
        print("INCORRECT VALUE.")
    choice_allocate = int(choice_allocate)

    while choice_allocate < 1 or choice_allocate > char.skill_points:
        print("You don't have that many!")
    print("SUCCESS")
    char.skills[skills[choice_skill]] += 5
    CheckSkillRewards(char, skills[choice_skill])

