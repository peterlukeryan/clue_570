#goals : instead of accuse method being called we have to signal player turn and then the player decides to accuse or not
# have a global flag to tell everyone else in game if accuse has been called and on who (and if its the game ending accusation or not)
# Also each player obj needs to maintain a list of all other players and their hands (deducing live)
# so then the player class gets to decide who to accuse based on this


import random
from Player import Player

# Initialize characters, weapons, rooms
characters = ["Dr. Orchid", "Mr. Green", "Col. Mustard", "Ms. Peacock", "Prof. Plum","Ms. Scarlett"]
weapons = ["Wrench", "Rope", "Steel Bar", "Knife", "Shovel", "Razor"]
rooms = ["Hall", "Piano Room", "Greenhouse", "Study", "Billiard Room", "Bedroom","Dining Room", "Library", "Kitchen"]

# Randomly select three cards, from each type-- as 'murder cards'
murder_cards = []

murder_character = random.choice(characters)
murder_weapon = random.choice(weapons)
murder_room = random.choice(rooms)


# Remove murder cards, recombine for 'shuffle'
new_characters = [c for c in characters if c != murder_character]
new_weapons = [w for w in weapons if w != murder_weapon]
new_rooms = [r for r in rooms if r != murder_room]

pooled_cards = new_characters + new_weapons + new_rooms

random.shuffle(pooled_cards)

num_players = 6  #can modify however
hands = [pooled_cards[i::num_players] for i in range(num_players)]  # Distribute cards evenly

players = []
for i in range(num_players):
    cur_player_map = dict()
    for j in range(num_players):
        if j != i:
            cur_player_map[j] = []
        else:
            cur_player_map[j] = hands[i]


    players.append(Player(player_map=cur_player_map, player_id=i))
    players[i].initialize_suspects()


for player in players:
    print(player.player_map)
    print("suspects: ")
    print(player.suspects)

# game_over = False
# turn = 0
#
# while not game_over:
#     # discard = ""
#
#     # accusation_index = 1
#     # while accusation_index <= num_players and discard == "":
#     #     discard = current_player.accuse(players[(turn + accusation_index) % num_players])
#     #     print("Player " + str((turn % num_players)+1) + " up")
#     #     print("Current discard: " + discard)
#     #     print("Player " + str((turn % num_players)+1) +"'s suspects")
#     #     print(current_player.suspect_list)
#     #     accusation_index += 1
#     # if discard:
#
#     #     if discard in current_player.suspect_list[0]:
#     #         current_player.suspect_list[0].remove(discard)
#     #     elif discard in current_player.suspect_list[1]:
#     #         current_player.suspect_list[1].remove(discard)
#     #     else:
#     #         current_player.suspect_list[2].remove(discard)
#     #     turn += 1
#     # else:
#     #     print("Player " + str(turn % num_players) +" won!")
#
#     #     game_over = True
#
#
#     # Player decides whether to accuse or not
#     # Like we wanted?
#
#
#
#
#     turn += 1