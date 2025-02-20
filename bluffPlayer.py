import random
class bluffPlayer:
    def __init__(self, player_id=None, player_map=None):
        self.player_map = player_map if player_map is not None else {}  # player map initializes as dictionary
        self.player_id = player_id  # Now using ids
        self.suspects = []

    def initialize_suspects(self):
        # Initialize deduction for each other player
        characters = ["Dr. Orchid", "Mr. Green", "Col. Mustard", "Ms. Peacock", "Prof. Plum", "Ms. Scarlett"]
        weapons = ["Wrench", "Rope", "Steel Bar", "Knife", "Shovel", "Razor"]
        rooms = ["Hall", "Piano Room", "Greenhouse", "Study", "Billiard Room", "Bedroom", "Dining Room", "Library",
                 "Kitchen"]
        hand = self.player_map[self.player_id]
        player_characters = list(set(hand) & set(characters))
        player_weapons = list(set(hand) & set(weapons))
        player_rooms = list(set(hand) & set(rooms))

        char_suspects = [character for character in characters if character not in player_characters]
        weapon_suspects = [weapon for weapon in weapons if weapon not in player_weapons]
        room_suspects = [room for room in rooms if room not in player_rooms]

        self.suspects = [char_suspects, weapon_suspects, room_suspects]

    def show_hand(self):
        return f"Player's hand: {self.player_map[self.player_id]}"

    def show_suspect_list(self):
        return f"Suspect list: {self.suspects}"

    def accuse(self, player, cards):
        # Check if the player wants to bluff (accuse cards they already have)
        bluff_cards = [card for card in cards if card in self.player_map[self.player_id]]
        if bluff_cards:
            # If bluffing, accuse one of the cards they already have
            return random.choice(bluff_cards)
        else:
            # If not bluffing, proceed with normal accusation
            return player.respond(cards)

    def respond(self, cards):
        for card in cards:
            if card in self.player_map[self.player_id]:
                return card
        return None
    
    def get_one_of_my_cards(self):
        characters = ["Dr. Orchid", "Mr. Green", "Col. Mustard", "Ms. Peacock", "Prof. Plum", "Ms. Scarlett"]
        weapons = ["Wrench", "Rope", "Steel Bar", "Knife", "Shovel", "Razor"]
        rooms = ["Hall", "Piano Room", "Greenhouse", "Study", "Billiard Room", "Bedroom", "Dining Room", "Library",
                 "Kitchen"]
        
        card = random.choice(self.player_map[self.player_id])
        if card in characters:
            print("Character card", card)
            return [0, card]
        elif card in weapons:
            print("Weapon card", card)    
            return [1, card]
        else:
            print("Room card", card)
            return [2, card]

    def make_accusation(self, players, turn, num_players):
        accusation_index = 1
        while accusation_index <= num_players:
            # accusation_cards = [self.suspects[0][0], self.suspects[1][0], self.suspects[2][0]] #hardcode one of the cards from my own hand in
            # that is the proposed fix
            bluff_card = self.get_one_of_my_cards()
            accusation_cards = None
            if bluff_card[0] == 0:
                accusation_cards = [bluff_card[1], self.suspects[1][0], self.suspects[2][0]]
            elif bluff_card[0] == 1:
                accusation_cards = [self.suspects[0][0], bluff_card[1], self.suspects[2][0]]
            else:
                accusation_cards = [self.suspects[0][0], self.suspects[1][0], bluff_card[1]]
            
            print( "BLUFF Accusation cards: -----------------")
            print(accusation_cards)
            discard = self.accuse(players[(turn + accusation_index) % num_players ], accusation_cards)
            if discard:
                print(discard)
                player_who_refuted = (turn + accusation_index) % num_players
                self.player_map[player_who_refuted].append(discard)

                if discard in self.suspects[0]:
                    self.suspects[0].remove(discard)
                elif discard in self.suspects[1]:
                    self.suspects[1].remove(discard)
                else:
                    self.suspects[2].remove(discard)
                print(self.show_suspect_list())
                return False
            accusation_index += 1
        if all(card not in self.player_map[self.player_id] for card in accusation_cards):
            print("Game over!")
            return True
        return False