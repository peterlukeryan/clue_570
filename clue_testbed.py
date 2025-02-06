#goals : play an entire game until the end
#player array (so can handle accusations and all in the game)

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
murder_cards = [murder_character, murder_weapon, murder_room]


# Remove murder cards, recombine for 'shuffle'
characters.remove(murder_character)
weapons.remove(murder_weapon)
rooms.remove(murder_room)

pooled_cards = characters + weapons + rooms
random.shuffle(pooled_cards)

# #Initialize 'player hands'
# print("Murder cards: ")
# print(murder_character + " with the " + murder_weapon + " in the " + murder_room)
# player_one_hand = pooled_cards[0:6]
# player_two_hand = pooled_cards[6:12]
# player_three_hand = pooled_cards[12:18]



# #Introduce 'suspect list'-- i.e all cards player-one doesn't know about
# suspect_list = [x for x in pooled_cards if x not in player_one_hand]


# player1 = Player(player_hand = player_one_hand, suspect_list = suspect_list)
# player2 = Player(player_hand = player_two_hand, suspect_list = suspect_list)

# print(player1.accuse(player2, ["Col. Mustard", "Drawing Room", "Shovel"]))

#^^^^^^^^^^^ didnt remove just in case

num_players = 3  #can modify however
hands = [pooled_cards[i::num_players] for i in range(num_players)]  # Distribute cards evenly

players = [] #the player array
for i in range(num_players):
    known_cards = hands[i]
    suspect_people = [char for char in characters if char not in known_cards]
    suspect_weapons = [wpn for wpn in weapons if wpn not in known_cards]
    suspect_rooms = [rm for rm in rooms if rm not in known_cards]

    players.append(Player(
        player_hand=known_cards,
        suspect_people=suspect_people,
        suspect_weapons=suspect_weapons,
        suspect_rooms=suspect_rooms
    ))

# murder scenario
print(f"Murder cards: {murder_character} with the {murder_weapon} in the {murder_room}")

# game loop
game_over = False
turn = 0

while not game_over:
    current_player = players[turn % num_players]
    print(f"\nPlayer {turn % num_players + 1}'s turn:")

    # accusing with random cards (for now)
    accusation = [
        random.choice(characters + [murder_character]),  
        random.choice(weapons + [murder_weapon]),        
        random.choice(rooms + [murder_room])             
    ]
    print(f"Accusing: {accusation}")

    # Check accusation against other players
    for other_player in players:
        if other_player != current_player:
            response = other_player.response(accusation)
            if response:
                print(f"Another player disproves with: {response}")
                break
    else:
        #check if the accusation is correct to end game
        if set(accusation) == set(murder_cards):
            print(f"Player {turn % num_players + 1} wins! The correct murder was {murder_cards}.")
            game_over = True
        else:
            print("No one disproves, but the accusation was incorrect!")

    turn += 1