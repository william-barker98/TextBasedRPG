def CheckModifiers(char):
    for key, value in char.buffs.items():
        print("VALUE: {}".format(char.buffs[key]))
        if value == 0:
            print("{} has expired.".format(key))
            RemoveModifiers(key, char)
        else:
            char.buffs[key] -= 1
            print("- Value: {}".format(char.buffs[key]))
            return

    for key, value in char.debuffs.items():
        print("VALUE: {}".format(char.debuffs[key]))
        if value == 0:
            print("{} has expired.".format(key))
            RemoveModifiers(key, char)
        else:
            char.debuffs[key] -= 1
            print("- Value: {}".format(char.debuffs[key]))
            return


def RemoveModifiers(key, char):
    if key == "Haste":
        char.agl -= 5
        char.buffs.pop(key)
    if key == "Rend":
        char.defense += char.defense
        char.debuffs.pop(key)

