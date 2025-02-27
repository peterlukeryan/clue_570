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

# Initialize win counters
win_counts = {i: 0 for i in range(num_players)}  # Track wins for each player

# Run 100 games
num_games = 1000
for game_num in range(num_games):
    print(f"\nGame {game_num + 1}/{num_games}")

    # Randomly select three cards, from each type-- as 'murder cards'
    murder_character = random.choice(characters)
    murder_weapon = random.choice(weapons)
    murder_room = random.choice(rooms)

    print("Murder scenario: ")
    print(f"Character: {murder_character}")
    print(f"Weapon: {murder_weapon}")
    print(f"Room: {murder_room}")

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
        print(f"\nTurn {turn}")
        if turn == 200:  # End game after 200 turns if no one wins
            game_over = True
            print("Game over! No one won.")
            break

        current_player = players[turn % num_players]
        print(f"Current player: {current_player.player_id} ({current_player.__class__.__name__})")
        print(f"Player's hand: {current_player.show_hand()}")
        print(f"Suspect list: {current_player.suspects}")

        # Check if current player's suspect list is fully narrowed down to the right accusation
        if len(current_player.suspects[0]) == 1 and len(current_player.suspects[1]) == 1 and len(current_player.suspects[2]) == 1:
            accusation = [current_player.suspects[0][0], current_player.suspects[1][0], current_player.suspects[2][0]]
            if accusation == [murder_character, murder_weapon, murder_room]:
                print(f"Player {current_player.player_id} won the game with: {accusation}")
                win_counts[current_player.player_id] += 1  # Increment win count for the winning player
                print(f"Updated win counts: {win_counts}")  # Debug statement
                game_over = True
            else:
                print(f"Player {current_player.player_id} made an incorrect accusation: {accusation}")
        else:
            # Make an accusation or reveal cards
            accusation_result = current_player.make_accusation(players, turn, num_players)
            if accusation_result:  # If the accusation is correct
                print(f"Player {current_player.player_id} won the game with their accusation!")
                win_counts[current_player.player_id] += 1  # Increment win count for the winning player
                print(f"Updated win counts: {win_counts}")  # Debug statement
            game_over = accusation_result  # Set game_over based on the accusation result

        turn += 1

# Print the results
print("\nGame Results:")
for player_id, wins in win_counts.items():
    player_type = players[player_id].__class__.__name__
    print(f"{player_type} (Player {player_id}) won {wins} times.")