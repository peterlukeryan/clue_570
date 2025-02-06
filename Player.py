#separate out the lists for weapon place and suspect
class Player:
    def __init__(self, player_hand=None, suspect_people=None, suspect_weapons=None, suspect_rooms=None):
        self.player_hand = player_hand if player_hand is not None else []
        self.suspect_people = suspect_people if suspect_people is not None else []
        self.suspect_weapons = suspect_weapons if suspect_weapons is not None else []
        self.suspect_rooms = suspect_rooms if suspect_rooms is not None else []

    def show_hand(self):
        return f"Player's hand: {self.player_hand}"

    def show_suspect_lists(self):
        return (f"Suspect People: {self.suspect_people}\n"
                f"Suspect Weapons: {self.suspect_weapons}\n"
                f"Suspect Rooms: {self.suspect_rooms}")

    def response(self, accused_cards):
        matching_cards = list(set(self.player_hand) & set(accused_cards))
        if not matching_cards:
            return ""
        else:
            return matching_cards[0]

    def accuse(self, player, cards):
        return player.response(cards)