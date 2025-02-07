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

num_players = 3  #can modify however
hands = [pooled_cards[i::num_players] for i in range(num_players)]  # Distribute cards evenly

players = []
for i in range(num_players):
    player_characters = list(set(hands[i]) & set(characters))
    player_weapons = list(set(hands[i]) & set(weapons))
    player_rooms = list(set(hands[i]) & set(rooms))

    char_suspects = [character for character in characters if character not in player_characters]
    weapon_suspects = [weapon for weapon in weapons if weapon not in player_weapons]
    room_suspects = [room for room in rooms if room not in player_rooms]
    players.append(Player(player_hand=[player_characters, player_weapons, player_rooms], suspect_list=[char_suspects, weapon_suspects, room_suspects]))

for player in players:
    print(player.show_hand())
    print("suspects")
    print(player.show_suspect_list())

#Initialize 'player hands'
print("Murder cards: ")
print(murder_character + " with the " + murder_weapon + " in the " + murder_room)
# player_one_hand = pooled_cards[0:6]
#
# # Create distinct arrays for each card type
# player_one_characters = list(set(player_one_hand) & set(characters))
# player_one_weapons = list(set(player_one_hand) & set(weapons))
# player_one_rooms = list(set(player_one_hand) & set(rooms))
#
#
# #create distinct arrays for each suspect type
# p1_character_suspects = [character for character in characters if character not in player_one_characters]
# p1_weapon_suspects = [weapon for weapon in weapons if weapon not in player_one_weapons]
# p1_room_suspects = [room for room in rooms if room not in player_one_rooms]
#
#
#
# player_two_hand = pooled_cards[6:12]
# player_three_hand = pooled_cards[12:18]
#
#
#
# #Introduce 'suspect list'-- i.e all cards player-one doesn't know about
# suspect_list = [x for x in pooled_cards if x not in player_one_hand]
#
#
# player1 = Player(player_hand = [player_one_characters, player_one_weapons, player_one_rooms], suspect_list = [p1_character_suspects, p1_weapon_suspects, p1_room_suspects])
# print(player1.show_hand())
# print(player1.show_suspect_list())
#
# player2 = Player(player_hand = player_two_hand, suspect_list = [p1_character_suspects, p1_weapon_suspects, p1_room_suspects])
#
#
# print(player1.accuse(player2))

