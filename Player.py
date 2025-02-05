class Player:
    def __init__(self, player_hand=None, suspect_list=None):
        self.player_hand = player_hand if player_hand is not None else []
        self.suspect_list = suspect_list if suspect_list is not None else []

    def show_hand(self):
        return f"Player's hand: {self.player_hand}"

    def show_suspect_list(self):
        return f"Suspect list: {self.suspect_list}"

    def response(self, accused_cards):
        matching_cards = list(set(self.player_hand) & set(accused_cards))
        if not matching_cards:
            return ""
        else:
            return matching_cards[0]

    def accuse(self, player):
        character_accusation = self.suspect_list[0][0]
        weapon_accusation = self.suspect_list[1][0]
        room_accusation = self.suspect_list[2][0]
        return player.response([character_accusation, weapon_accusation, room_accusation])