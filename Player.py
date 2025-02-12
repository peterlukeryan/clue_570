class Player:
    def __init__(self, player_hand=None, suspect_list=None, player_id=None):
        self.player_hand = player_hand if player_hand is not None else [[], [], []]  # Characters, Weapons, Rooms
        self.suspect_list = suspect_list if suspect_list is not None else [[], [], []]  # Characters, Weapons, Rooms
        self.player_id = player_id  # Now using ids 
        self.deduction = {}  
        self.other_players = []  # List of other players in the game

    def initialize_deduction(self, players):
        # Initialize deduction for each other player
        for player in players:
            if player.player_id != self.player_id:  # do for all except self
                self.deduction[player.player_id] = {
                    "characters": set(self.suspect_list[0]),  # characters
                    "weapons": set(self.suspect_list[1]),     #weapons
                    "rooms": set(self.suspect_list[2])        #rooms
                }

    def show_hand(self):
        return f"Player's hand: {self.player_hand}"

    def show_suspect_list(self):
        return f"Suspect list: {self.suspect_list}"

    def response(self, accused_cards):
        matching_cards = [card for category in self.player_hand for card in category if card in accused_cards]

        if not matching_cards:
            return ""
        else:
            print(f"Player {self.player_id} refutes with {matching_cards[0]}")
            return matching_cards[0]  # Return the first matching card

    def accuse(self, player):
        # Accuse another player with the first suspect in each category
        character_accusation = self.suspect_list[0][0]
        weapon_accusation = self.suspect_list[1][0]
        room_accusation = self.suspect_list[2][0]
        print(f"Player {self.player_id} accuses Player {player.player_id} with {character_accusation}, {weapon_accusation}, {room_accusation}")
        return player.response([character_accusation, weapon_accusation, room_accusation])

    def update_deduction(self, card, player):
        # Update deduction for the player who responded
        if card in self.suspect_list[0]:  #Chara
            self.deduction[player.player_id]["characters"].discard(card)
        elif card in self.suspect_list[1]:  # Weapon
            self.deduction[player.player_id]["weapons"].discard(card)
        elif card in self.suspect_list[2]:  # Room
            self.deduction[player.player_id]["rooms"].discard(card)

    def decide_to_accuse(self):
        # Decide which player to accuse based on the number of unknown cards they have
        max_unknown = -1
        accused_player = None

        for player_id, deduction in self.deduction.items():
            unknown_count = len(deduction["characters"]) + len(deduction["weapons"]) + len(deduction["rooms"])
            if unknown_count > max_unknown:
                max_unknown = unknown_count
                accused_player = next(player for player in self.other_players if player.player_id == player_id)

        return accused_player
    
    # Changed this up almost completely 