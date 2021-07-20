import random


class Enemies:
    def __init__(self, name):
        self.name = name
        self.type = type
        self.initiative = 0
        self.dead = False
        if name == "Goblin":
            self.health = 14
            self.max_health = 14
            self.atk = 10
            self.defense = 12
            self.agl = 12
            self.gold = 5
            self.exp = 6
            self.lvl = 1
            self.drop_chance = 20
            self.drop_items = ["Medicinal Herb"]
            self.actions = ['ATTACK', 'IDLE']
            self.res = {'Fire': 4, 'Shock': 3}

        if name == "Wolf":
            self.max_health = 12
            self.health = 12
            self.atk = 14
            self.defense = 10
            self.agl = 24
            self.gold = 2
            self.exp = 4
            self.lvl = 1
            self.drop_chance = 20
            self.drop_items = ["Medicinal Herb"]
            self.actions = ['ATTACK', 'CRIT']
            self.res = {'Fire': 1, 'Shock': 2}


    def action(self, player):
        if self.health <= 0:
            pass
        else:
            action = random.choice(self.actions)
            if action == "ATTACK":
                self.attack(False, player)
            if action == "CRIT":
                self.attack(True, player)
            if action == "IDLE":
                print(self.name, "is idle.")
                pass



    def attack(self, crit, player):
        # Select party member to attack
        targets = []
        if player.dead is False:
            targets = [player]
        else:
            pass
        for a in player.allies:
            if a.dead is False:
                targets.append(a)
            else:
                pass
        target = random.choice(targets)

        dmg_mod = random.randint(1, 6)
        dmg_dealt = self.atk + dmg_mod - target.defense
        if dmg_dealt < 1:
            dmg_dealt = 1
        target.health -= dmg_dealt
        print("{} attacks {} for {} damage!".format(self.name, target.name, dmg_dealt))
        if target.health <= 0:
            if target.dead is True:
                pass

            print("{} has been slain :'(".format(target.name))
            target.dead = True
            targets.remove(target)


