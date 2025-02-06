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

# Remove murder cards, recombine for 'shuffle'
characters.remove(murder_character)
weapons.remove(murder_weapon)
rooms.remove(murder_room)

pooled_cards = characters + weapons + rooms
random.shuffle(pooled_cards)

#Initialize 'player hands'
print("Murder cards: ")
print(murder_character + " with the " + murder_weapon + " in the " + murder_room)
player_one_hand = pooled_cards[0:6]
player_two_hand = pooled_cards[6:12]
player_three_hand = pooled_cards[12:18]



#Introduce 'suspect list'-- i.e all cards player-one doesn't know about
suspect_list = [x for x in pooled_cards if x not in player_one_hand]


player1 = Player(player_hand = player_one_hand, suspect_list = suspect_list)
player2 = Player(player_hand = player_two_hand, suspect_list = suspect_list)

print(player1.accuse(player2, ["Col. Mustard", "Drawing Room", "Shovel"]))

