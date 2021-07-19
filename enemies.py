import random


class Enemies:
    def __init__(self, type, game, player):
        self.game = game
        self.type = type
        if type == "Goblin":
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

        if type == "Wolf":
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

    def action(self, player):
        action = random.choice(self.actions)
        if action == "ATTACK":
            self.attack(False, player)
        if action == "CRIT":
            self.attack(True, player)
        if action == "IDLE":
            pass

        pass

    def attack(self, crit, player):
        dmg_mod =  random.randint(1, 6)
        dmg_dealt = self.atk + dmg_mod - player.defense
        if dmg_dealt < 1:
            dmg_dealt = 1
        player.health -= dmg_dealt
        print("{} attacks for {} damage!".format(self.type, dmg_dealt))
        pass


