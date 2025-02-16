import random
import pickle
from Player import Player
from bluffPlayer import bluffPlayer
from deducedbluffPlayer import deducedbluffPlayer
from rl_Player import RLPlayer  # Import the RLPlayer class

# Initialize characters, weapons, rooms
characters = ["Dr. Orchid", "Mr. Green", "Col. Mustard", "Ms. Peacock", "Prof. Plum", "Ms. Scarlett"]
weapons = ["Wrench", "Rope", "Steel Bar", "Knife", "Shovel", "Razor"]
rooms = ["Hall", "Piano Room", "Greenhouse", "Study", "Billiard Room", "Bedroom", "Dining Room", "Library", "Kitchen"]

# Number of players
num_players = 6

# Create the RLPlayer instance and load the trained Q-table
rl_player = RLPlayer(player_id=0)
with open("q_table.pkl", "rb") as f:
    rl_player.q_table = pickle.load(f)

# Randomly select three cards, from each type-- as 'murder cards'
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

hands = [pooled_cards[i::num_players] for i in range(num_players)]  # Distribute cards evenly

# Define the specific player types
player_types = [rl_player, bluffPlayer(), deducedbluffPlayer()]  # RLPlayer, bluffPlayer, deducedbluffPlayer
player_types.extend([Player() for _ in range(num_players - 3)])  # The rest are regular Players
random.shuffle(player_types)  # Shuffle player types for random order

# Create players based on the specified types
players = []
for i in range(num_players):
    cur_player_map = dict()
    for j in range(num_players):
        if j != i:
            cur_player_map[j] = []
        else:
            cur_player_map[j] = hands[i]

    player_class = player_types[i]
    players.append(player_class)
    players[i].player_map = cur_player_map
    players[i].player_id = i
    players[i].initialize_suspects()

# Print player hands for debugging
for player in players:
    print(f"Player {player.player_id} hand: {player.player_map[player.player_id]}")

print("Start game")
game_over = False
turn = 0

while not game_over:
    print(f"Turn {turn}")
    if turn == 200:  # End game after 200 turns if no one wins
        game_over = True
        print("Game over! No one won.")
        break

    current_player = players[turn % num_players]
    print(f"Current player: {current_player.player_id} ({current_player.__class__.__name__})")
    print(current_player.show_hand())

    # Check if current player's suspect list is fully narrowed down to the right accusation
    if len(current_player.suspects[0]) == 1 and len(current_player.suspects[1]) == 1 and len(current_player.suspects[2]) == 1:
        print(f"Player {current_player.player_id} won the game with: {current_player.suspects[0][0]}, {current_player.suspects[1][0]}, {current_player.suspects[2][0]}")
        game_over = True
    else:
        # Make an accusation or reveal cards
        game_over = current_player.make_accusation(players, turn, num_players)

    turn += 1