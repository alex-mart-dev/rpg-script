import random
import math


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\0334m'


class Person:
    def __init__(self,name, hp, mp, atk, int, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.int = int
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def elix(self):
        self.hp = self.maxhp
        self.mp = self.maxmp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def get_health(self):
        health = self.hp / self.maxhp * 100
        return health

    def choose_action(self):
        i = 1
        print(bcolors.OKGREEN + "Actions" + bcolors.END)
        for item in self.actions:
            print("  ", str(i) + ":" + item)
            i += 1

    def choose_magic(self):
        i = 1
        print(bcolors.OKGREEN + "Magic" + bcolors.END)
        for spell in self.magic:
            print("    " + str(i) + ":", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("Items")
        for item in self.items:
            print(str(i) + ":", item["item"].name, ":", item["item"].desc + " (x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "Target:" + bcolors.END)
        for enemy in enemies:
            print("    " + str(i) + "." + enemy.name)
            i += 1
        choice = int(input("Choose target ")) - 1
        return choice

    def choose_ally(self, players):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "Ally:" + bcolors.END)
        for player in players:
            print("    " + str(i) + "." + player.name)
            i += 1
        choice = int(input("Choose ally ")) - 1
        return choice

    def get_stats(self):
        hp_blocks = math.floor(self.hp / self.maxhp * 25)
        invhp = 25 - hp_blocks
        mp_blocks = math.ceil(self.mp / self.maxmp * 10)
        invmp = 10 - mp_blocks
        name_space = 8 - len(self.name)
        hp_space = 8 - len(str(self.maxhp) + str(self.hp))
        mp_space = 7 - len(str(self.maxmp)) - len(str(self.mp))

        # special whitespace character used to match closely block width
        print(self.name + name_space * " " + str(self.hp) + "/" + str(self.maxhp) +
              "      " + hp_space * " " + bcolors.OKGREEN + "|" + hp_blocks * "█" + invhp * " " +
              "|   " + bcolors.END + str(self.mp) + "/" + str(self.maxmp) + mp_space * " " + "|" +
              bcolors.OKBLUE + mp_blocks * "█" + invmp * " " + "|" + bcolors.END)
