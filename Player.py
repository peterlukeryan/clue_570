class Player:
<<<<<<< Updated upstream
    def __init__(self, player_hand=None, suspect_list=None):
        self.player_hand = player_hand if player_hand is not None else [[], [], []]
        self.suspect_list = suspect_list if suspect_list is not None else [[], [], []]  # Keep list of lists
=======
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
>>>>>>> Stashed changes

    def show_hand(self):
        return f"Player's hand: {self.player_hand}"

    def show_suspect_list(self):
        return f"Suspect list: {self.suspect_list}"

<<<<<<< Updated upstream
    def response(self, accused_cards):
        # Instead of using set(self.player_hand), check membership in each inner list
        matching_cards = [card for category in self.player_hand for card in category if card in accused_cards]

        if not matching_cards:
            return ""
        else:
            print(f"Character refutes with {matching_cards[0]}")
            return matching_cards[0]

    def accuse(self, player):
        character_accusation = self.suspect_list[0][0]
        weapon_accusation = self.suspect_list[1][0]
        room_accusation = self.suspect_list[2][0]
        print(f"Player accuses with {character_accusation} {weapon_accusation} {room_accusation}")
        return player.response([character_accusation, weapon_accusation, room_accusation])
=======
    def accuse(self, player, cards):
        return player.respond(cards)

    def respond(self, cards):
        for card in cards:
            if card in self.player_map[self.player_id]:
                return card
        return None

    def make_accusation(self, players, turn, num_players):
        accusation_index = 1
        while accusation_index <= num_players:
            accusation_cards = [self.suspects[0][0], self.suspects[1][0], self.suspects[2][0]]
            print("Accusation cards:")
            print(accusation_cards)
            discard = self.accuse(players[(turn + accusation_index) % num_players], accusation_cards)
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
>>>>>>> Stashed changes
