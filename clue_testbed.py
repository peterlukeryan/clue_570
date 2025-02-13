import random
from Player import Player
from bluffPlayer import bluffPlayer
from deducedbluffPlayer import deducedbluffPlayer

# Initialize characters, weapons, rooms
characters = ["Dr. Orchid", "Mr. Green", "Col. Mustard", "Ms. Peacock", "Prof. Plum", "Ms. Scarlett"]
weapons = ["Wrench", "Rope", "Steel Bar", "Knife", "Shovel", "Razor"]
rooms = ["Hall", "Piano Room", "Greenhouse", "Study", "Billiard Room", "Bedroom", "Dining Room", "Library", "Kitchen"]

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

num_players = 6  # can modify however
hands = [pooled_cards[i::num_players] for i in range(num_players)]  # Distribute cards evenly

# Define the number of each player type
num_normal_players = 2
num_bluff_players = 2
num_deduced_bluff_players = 2

# Create players based on the specified types
players = []
player_types = (
    [Player] * num_normal_players +
    [bluffPlayer] * num_bluff_players +
    [deducedbluffPlayer] * num_deduced_bluff_players
)
random.shuffle(player_types)  # Shuffle player types for random order

for i in range(num_players):
    cur_player_map = dict()
    for j in range(num_players):
        if j != i:
            cur_player_map[j] = []
        else:
            cur_player_map[j] = hands[i]

    player_class = player_types[i]
    players.append(player_class(player_map=cur_player_map, player_id=i))
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
    current_player = players[turn % num_players]
    print(current_player.show_hand())
    # check if current player's suspect list is fully down to the right accusation
    if len(current_player.suspects[0]) == 1 and len(current_player.suspects[1]) == 1 and len(
            current_player.suspects[2]) == 1:
        print("Current player won the game with: " + current_player.suspects[0][0] + " " + current_player.suspects[1][0] + " " + current_player.suspects[2][0])
        game_over = True
    else:
        game_over = current_player.make_accusation(players, turn, num_players)
    turn += 1