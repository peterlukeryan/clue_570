class Player:
    def __init__(self, player_hand=None, suspect_list=None):
        self.player_hand = player_hand if player_hand is not None else [[], [], []]
        self.suspect_list = suspect_list if suspect_list is not None else [[], [], []]  # Keep list of lists
        self.accusations_made = 0
        self.cards_revealed = 0

    def show_hand(self):
        return f"Player's hand: {self.player_hand}"

    def show_suspect_list(self):
        return f"Suspect list: {self.suspect_list}"

    def response(self, accused_cards):
        # Instead of using set(self.player_hand), check membership in each inner list
        matching_cards = [card for category in self.player_hand for card in category if card in accused_cards]
        if matching_cards:
            self.record_revealed_card()
            print(f"Character refutes with {matching_cards[0]}")
            return matching_cards[0]
        return ""


    def accuse(self, player):
        self.record_accusation()
        character_accusation = self.suspect_list[0][0]
        weapon_accusation = self.suspect_list[1][0]
        room_accusation = self.suspect_list[2][0]
        print(f"Player accuses with {character_accusation} {weapon_accusation} {room_accusation}")
        return player.response([character_accusation, weapon_accusation, room_accusation])

    def record_accusation(self):
        self.accusations_made += 1

    def record_revealed_card(self):
        self.cards_revealed += 1

    def show_metrics(self):
        return f"Accusations Made: {self.accusations_made}, Cards Revealed: {self.cards_revealed}"