#one of the deduced cards to bluff with is the shortest list in the suspects, annd then just use one rando card from that

class deducedbluffPlayer:
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
        # Advanced bluffing: Accuse cards that the player knows another player has
        known_cards = []
        for card in cards:
            for player_id, hand in self.player_map.items():
                if player_id != self.player_id and card in hand:
                    known_cards.append(card)
                    break

        if known_cards:
            # If the player knows another player has one of the accused cards, accuse it
            return random.choice(known_cards)
        else:
            # If no known cards, proceed with normal accusation
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