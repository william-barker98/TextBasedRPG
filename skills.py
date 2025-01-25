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
    if hasattr(char, "allies"):  # if player
        if skill == "Swords":
            if char.skills[skill] >= 5 and "Rend" not in char.abilities:
                char.abilities.append("Rend")
                print("You have learned Rend!")

    elif char.name == "Edgar":
        if skill == "Axes":
            if char.skills[skill] >= 5 and "Ratchet Man" not in char.abilities:
                char.abilities.append("Ratchet Man")
                print("{} has learned Ratchet Man!".format(char.name))

    elif char.name == "Katie":
        if skill == "Whips":
            pass
        elif skill == "Staves":
            if char.skills[skill] >= 5 and "Sizz" not in char.abilities:
                char.abilities.append("Sizz")
                print("{} has learned Sizz!".format(char.name))
        elif skill == "Allure":
            pass

    elif char.name == "Yorkshire":
        if skill == "Swords":
            pass
        elif skill == "Bows":
            pass
        elif skill == "Charisma":
            pass


def AllocateSkillPoints(char, points):
    skills = list(char.skills)
    values = char.skills.values()
    i = 1
    print("{} has [{}] skill points.\n".format(char.name, char.skill_points))
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

    choice_allocate = input("How many would you like to allocate? [{}]".format(char.skill_points))
    while not choice_allocate.isdigit():
        print("INCORRECT VALUE.")
    choice_allocate = int(choice_allocate)

    while choice_allocate < 1 or choice_allocate > char.skill_points:
        print("You don't have that many!")
    print("SUCCESS")
    char.skills[skills[choice_skill]] += 5
    CheckSkillRewards(char, skills[choice_skill])
