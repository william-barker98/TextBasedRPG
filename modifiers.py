def CheckModifiers(char):
    for key, value in char.buffs.items():
        print("VALUE: {}".format(value))
        if value == 0:
            print("{} has expired.".format(key))
            RemoveModifiers(key, char)
        else:
            char.buffs[key] -= 1
            print("- Value: {}".format(value))
            return


def RemoveModifiers(key, char):
    if key == "Haste":
        char.agl -= 5
