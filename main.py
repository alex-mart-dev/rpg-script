from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# create damage spells
fire = Spell("Fire", 10, 100, "black", "single")
thunder = Spell("Thunder", 12, 120, "black", "single")
blizzard = Spell("Blizzard", 15, 100, "black", "all")
quake = Spell("Quake", 20, 150, "black", "all")
meteor = Spell("Meteor", 25, 250, "black", "all")

# create healing spells
cure = Spell("Cure", 12, 120, "white", "single")
cura = Spell("Cura", 18, 200, "white", "single")
curall = Spell("Curall", 30, 200, "white", "all")

# return option for magic

back_magic = Spell("Go back", 0, 0, "back", "")

# create items
potion = Item("Potion", "potion", "Heals 50HP", 50, "single")
hipotion = Item("Hi-Potion", "potion", "Heals 100HP", 100, "single")
superpotion = Item("Super potion", "potion", "Heals 500hp", 500, "single")
elixir = Item("Elixer", "elixir", "Restores all HP/MP of one party member", 1, "single")
megaelixir = Item("Mega Elixir", "elixir", "Restores everyone's HP/MP", 1, "all")

# create damage items
grenade = Item("Grenade", "attack", "Deals 150 damage", 150, "single")
firebomb = Item("Fire Bomb", "attack", "Deals 250 damage to all enemies", 250, "all")

# return option for items

back_items = Item("Go back", "back", "", 0, "")

allspells =[fire, thunder, blizzard, meteor, quake, cure, cura, curall, back_magic]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixir, "quantity": 5},
                {"item": megaelixir, "quantity": 2}, {"item": grenade, "quantity": 5},
                {"item": firebomb, "quantity": 1}, {"item": back_items, "quantity": 9999}]
# Instantiate people
player1 = Person("Isaac", 440, 80, 60, 1, allspells, player_items)
player2 = Person("Garett", 560, 40, 100, 0.8, allspells, player_items)
player3 = Person("Ivan", 300, 220, 35, 1.4, allspells, player_items)

enemy1 = Person("Flame", 1200, 200, 30, 1.2, allspells, [])
enemy2 = Person("Mars", 2500, 65, 45, 1, [allspells], [])
enemy3 = Person("Slash", 1250, 20, 100, 0.5, [fire, cure], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "TIME TO BATTLE!" + bcolors.END)

while running:
    print("================")
    print(bcolors.BOLD + bcolors.OKGREEN + "NAME                   " + "HP" + bcolors.OKBLUE
          + "                                                  MP" + bcolors.END)
    for player in players:
        player.get_stats()

    print("\n")
    print(bcolors.BOLD + bcolors.FAIL + "FOES                    " + bcolors.OKGREEN + "HP" + bcolors.OKBLUE
          + "                                                  MP" + bcolors.END)

    for enemy in enemies:
        enemy.get_stats()

    for player in players:
        print("\n")
        print(bcolors.BOLD + bcolors.OKGREEN + player.name.upper() + ":" + bcolors.END)
        player.choose_action()
        choice = input("Choose action ")
        index = int(choice) - 1
        print("You choose:", player.actions[index])

        if index == 0:
            dmg = player.generate_damage()
            target = player.choose_target(enemies)
            enemies[target].take_damage(dmg)
            if enemies[target].get_hp() == 0:
                print(bcolors.OKBLUE + player.name, "deals a fatal blow to " + enemies[target].name + bcolors.END)
                del enemies[target]
            else:
                print(bcolors.OKBLUE + player.name, "deals", dmg, "damage to " + enemies[target].name + bcolors.END)

        if index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose a spell ")) - 1

            spell = player.magic[magic_choice]
            magic_dmg = int(spell.generate_damage() * player.int)

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nYou don't have enough power left to cast this spell\n" + bcolors.END)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                if spell.target == "all":
                    for player in players:
                        player.heal(magic_dmg)
                        print(bcolors.OKGREEN + player.name, "Heals for", spell.dmg, "points")
                else:
                    ally = player.choose_ally(players)
                    players[ally].heal(magic_dmg)
                    print(players[ally].name, "is healed for", spell.dmg, "points")

            if spell.type == "black":
                if spell.target == "all":
                    i = 0
                    for enemy in enemies:
                        enemy.take_damage(magic_dmg)
                        if enemy.get_hp() == 0:
                            print(bcolors.OKBLUE + player.name,
                                  "deals a fatal blow to " + enemy.name + bcolors.END)
                            del enemies[i]
                        else:
                            print(spell.name, "deals", str(spell.dmg), "damage to", enemy.name)
                        i += 1
                else:
                    target = player.choose_target(enemies)
                    enemies[target].take_damage(magic_dmg)
                    if enemies[target].get_hp() == 0:
                        print(bcolors.OKBLUE + player.name, "deals a fatal blow to " + enemies[target].name + bcolors.END)
                        del enemies[target]
                    else:
                        print(spell.name, "deals", str(spell.dmg), "damage to", enemies[target].name)

            elif spell.type == "back":
                continue

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose an item ")) - 1

            item_chosen = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] <= 0:
                print(bcolors.FAIL + "You don't have enough", item_chosen.name + "s" + bcolors.END)
                continue

            else:
                player.items[item_choice]["quantity"] -= 1

                if item_chosen.type == "potion":
                    player.heal(item_chosen.prop)
                    print(bcolors.OKGREEN + "You heal for", item_chosen.prop, "points" + bcolors.END)

                if item_chosen.type == "elixir":
                    if item_chosen.target == "all":
                        for player in players:
                            player.elix()

                    else:
                        ally = player.choose_ally(players)
                        players[ally].elix()
                        print(players[ally].name, "has been restored to full health!")

                if item_chosen.type == "attack":
                    if item_chosen.target == "all":
                        i = 0
                        for enemy in enemies:
                            enemy.take_damage(item_chosen.prop)
                            if enemy.get_hp() == 0:
                                print(bcolors.OKBLUE + player.name,
                                      "deals a fatal blow to " + enemy.name + bcolors.END)
                                del enemies[i]
                            else:
                                print(item_chosen.name, "deals", item_chosen.prop, "damage to", enemy.name)
                            i += 1
                    else:
                        target = player.choose_target(enemies)
                        enemies[target].take_damage(item_chosen.prop)
                        if enemies[target].get_hp() == 0:
                            print(bcolors.OKBLUE + player.name,
                                  "deals a fatal blow to " + enemies[target].name + bcolors.END)
                            del enemies[target]
                        else:
                            print(bcolors.OKBLUE + "Your", item_chosen.name, "deals", item_chosen.prop,
                                  "damage", bcolors.END)

                elif item_chosen.type == "back":
                    continue


        print("================")
        print(bcolors.BOLD + bcolors.OKGREEN + "NAME                   " + "HP" + bcolors.OKBLUE
              + "                                                  MP" + bcolors.END)
        for player in players:
            player.get_stats()

        print("\n")
        print(bcolors.BOLD + bcolors.FAIL + "FOES                    " + bcolors.OKGREEN + "HP" + bcolors.OKBLUE
              + "                                                  MP" + bcolors.END)

        for enemy in enemies:
            enemy.get_stats()

    if len(enemies) != 0:
        for enemy in enemies:
            target = random.randrange(0, len(players))
            enemy_damage = enemy.generate_damage()
            players[target].take_damage(enemy_damage)
            if players[target].get_hp() == 0:
                print(bcolors.FAIL + enemy.name, "has dealt a fatal blow to",
                      players[target].name + bcolors.END)
                del players[target]
            else:
                print(bcolors.FAIL + enemy.name, "attacks", players[target].name,
                      "for", enemy_damage, "damage" + bcolors.END)
                """if enemy.get_health() > 30:
                if enemy.mp >= 12:
                    attack_method = random.randrange(0, 10)
                    if attack_method >= 4:
                        target = random.randrange(0, len(players))
                        enemy_damage = enemy.generate_damage()
                        players[target].take_damage(enemy_damage)
                        if players[target].get_hp() == 0:
                            print(bcolors.FAIL + enemy.name, "has dealt a fatal blow to",
                                  players[target].name + bcolors.END)
                            del players[target]
                        else:
                            print(bcolors.FAIL + enemy.name, "attacks", players[target].name,
                             "for", enemy_damage, "damage" + bcolors.END)
                    else:
                        casting = True
                        while casting:
                            magic_choice = random.randrange(0, len(enemy.magic))
                            spell = enemy.magic[magic_choice]

                            if spell.type != "black":
                                continue

                            current_mp = enemy.get_mp()

                            if spell.cost > current_mp:
                                continue

                            enemy.reduce_mp(spell.cost)
                            magic_dmg = int(spell.generate_damage() * enemy.int)

                            if spell.target == "all":
                                i = 0
                                for player in players:
                                    player.take_damage(magic_dmg)
                                    if player.get_hp() == 0:
                                        print(bcolors.OKBLUE + enemy.name,
                                              "deals a fatal blow to " + player.name + bcolors.END)
                                        del player[i]
                                    else:
                                        print(spell.name, "deals", str(spell.dmg), "damage to", player.name)
                                    i += 1
                                casting = False

                            else:
                                target = random.randrange(0, len(players))
                                players[target].take_damage(magic_dmg)
                                if players[target].get_hp() == 0:
                                    print(bcolors.OKBLUE + enemy.name,
                                          "deals a fatal blow to " + players[target].name + bcolors.END)
                                    del players[target]
                                else:
                                    print(spell.name, "deals", str(spell.dmg), "damage to", players[target].name)
                                casting = False

                else:
                    target = random.randrange(0, len(players))
                    enemy_damage = enemy.generate_damage()
                    players[target].take_damage(enemy_damage)
                    if players[target].get_hp() == 0:
                        print(bcolors.FAIL + enemy.name, "has dealt a fatal blow to",
                              players[target].name + bcolors.END)
                        del players[target]
                    else:
                        print(bcolors.FAIL + enemy.name, "attacks", players[target].name,
                              "for", enemy_damage, "damage" + bcolors.END)

            if enemy.get_health() <= 30:
                if enemy.mp >= 12:
                    casting = True
                    while casting:
                        magic_choice = random.randrange(0, len(enemy.magic))
                        spell = enemy.magic[magic_choice]

                        if spell.type != "white":
                            continue

                        magic_dmg = int(spell.generate_damage() * player.int)

                        current_mp = enemy.get_mp()

                        if spell.cost > current_mp:
                            continue

                        enemy.reduce_mp(spell.cost)

                        if spell.target == "all":
                            for enemy in enemies:
                                enemy.heal(magic_dmg)
                                print(bcolors.OKGREEN + enemy.name, "Heals for", spell.dmg, "points")
                                casting = False
                        else:
                            enemy.heal(magic_dmg)
                            print(bcolors.OKGREEN + enemy.name, "Heals for", spell.dmg, "points")
                            casting = False

                else:
                    target = random.randrange(0, len(players))
                    enemy_damage = enemy.generate_damage()
                    players[target].take_damage(enemy_damage)
                    if players[target].get_hp() == 0:
                        print(bcolors.FAIL + enemy.name, "has dealt a fatal blow to",
                              players[target].name + bcolors.END)
                        del players[target]
                    else:
                        print(bcolors.FAIL + enemy.name, "attacks", players[target].name,
                              "for", enemy_damage, "damage" + bcolors.END)"""


    if len(enemies) == 0:
        print(bcolors.OKBLUE + "You win!" + bcolors.END)
        running = False

    if len(players) == 0:
        print(bcolors.FAIL + "You have been defeated..." + bcolors.END)
        running = False
