#goals : instead of accuse method being called we have to signal player turn and then the player decides to accuse or not
# have a global flag to tell everyone else in game if accuse has been called and on who (and if its the game ending accusation or not)
# Also each player obj needs to maintain a list of all other players and their hands (deducing live)
 main


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

print("Murder scenario: ")
print(murder_character)
print(murder_weapon)
print(murder_room)

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




print("start game")
game_over = False
turn = 0

while not game_over:
    print(turn)
    if turn == 200:
        game_over = True
    discard = ""
    current_player = players[turn % num_players]
    print(current_player.show_hand())
    # check if current player's suspect list is fully down to the right accusation
    if len(current_player.suspects[0]) == 1 and len(current_player.suspects[1]) == 1 and len(
            current_player.suspects[2]) == 1:
        print("Current player won the game with: " + current_player.suspects[0][0] + " " + current_player.suspects[1][0] + " " + current_player.suspects[2][0])
        game_over = True
    accusation_index = 1
    while accusation_index <= num_players and not discard:
        accusation_cards = [current_player.suspects[0][0], current_player.suspects[1][0], current_player.suspects[2][0] ]
        print("Accusation cards:")
        print(accusation_cards)
        discard = current_player.accuse(players[(turn + accusation_index) % num_players], accusation_cards)
        accusation_index += 1
    if discard:
        print(discard)
        player_who_refuted = (turn + accusation_index) % num_players
        current_player.player_map[player_who_refuted].append(discard)

        if discard in current_player.suspects[0]:
            current_player.suspects[0].remove(discard)
        elif discard in current_player.suspects[1]:
            current_player.suspects[1].remove(discard)
        else:
            current_player.suspects[2].remove(discard)
        print(current_player.show_suspect_list())
        turn += 1
    else:
        if all(card not in current_player.player_map[current_player.player_id] for card in accusation_cards):
            print("Game over!")
            game_over = True
        turn += 1


    # Player decides whether to accuse or not
    # Like we wanted?




