from abc import ABC, abstractmethod

class Player(ABC):
    player_hand = []
    suspect_list = []

    #Accuse will be the same across all players/bots
    def accuse(player, suspected_cards):
        return player.response(suspected_cards)

    @abstractmethod
    def response(self):
        pass
