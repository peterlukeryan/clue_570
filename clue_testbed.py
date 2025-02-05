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

# Create distinct arrays for each card type
player_one_characters = list(set(player_one_hand) & set(characters))
player_one_weapons = list(set(player_one_hand) & set(weapons))
player_one_rooms = list(set(player_one_hand) & set(rooms))


#create distinct arrays for each suspect type
p1_character_suspects = [character for character in characters if character not in player_one_characters]
p1_weapon_suspects = [weapon for weapon in weapons if weapon not in player_one_weapons]
p1_room_suspects = [room for room in rooms if room not in player_one_rooms]



player_two_hand = pooled_cards[6:12]
player_three_hand = pooled_cards[12:18]



#Introduce 'suspect list'-- i.e all cards player-one doesn't know about
suspect_list = [x for x in pooled_cards if x not in player_one_hand]


player1 = Player(player_hand = [player_one_characters, player_one_weapons, player_one_rooms], suspect_list = [p1_character_suspects, p1_weapon_suspects, p1_room_suspects])
player2 = Player(player_hand = player_two_hand, suspect_list = [p1_character_suspects, p1_weapon_suspects, p1_room_suspects])


print(player1.accuse(player2))

