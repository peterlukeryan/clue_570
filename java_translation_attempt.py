import random
from typing import List, Dict
#attempting to translate that repo
#unfinished and simplified

class Cards:
    def __init__(self, info_on_card: str):
        self.info_on_card = info_on_card

    def __str__(self):
        return self.info_on_card

class DeckOfCardsTotal:
    def __init__(self):
        self.random = random.SystemRandom()
        self.cards_total_num = 21
        self.characters_total_num = 6
        self.tools_total_num = 6
        self.rooms_total_num = 9

        self.cards_info_origin = [
            "Dr.Orchid", "Mr.Green", "Col.Mustard", "Ms.Peacock", "Prof.Plum", "Mr.Scarlet",
            "wrench", "rope", "steel bar", "knife", "shovel", "razor",
            "piano room", "greenhouse", "billiard's room", "library", "study room", "hall", "bedroom", "dining", "kitchen"
        ]

        self.characters_array_of_names = ["Dr.Orchid", "Mr.Green", "Col.Mustard", "Ms.Peacock", "Prof.Plum", "Mr.Scarlet"]
        self.tools_array_of_names = ["wrench", "rope", "steel bar", "knife", "shovel", "razor"]
        self.rooms_array_of_names = ["piano room", "greenhouse", "billiard's room", "library", "study room", "hall", "bedroom", "dining", "kitchen"]

        self.all_of_cards_list = [None] * (self.cards_total_num - 3)
        self.characters_name_list = [None] * self.characters_total_num
        self.tools_name_list = [None] * self.tools_total_num
        self.rooms_name_list = [None] * self.rooms_total_num

        self.current_card = 0

        self.murderer_char = self.rand_select_murderer()
        self.murder_tool = self.rand_select_murder_tool()
        self.murder_room = self.rand_select_murder_room()

        self.string_based_18_cards = [None] * 18

    def shuffle_array_size_18(self):
        dynamic_cards_info = list(self.cards_info_origin)
        dynamic_cards_info.remove(self.murderer_char)
        dynamic_cards_info.remove(self.murder_tool)
        dynamic_cards_info.remove(self.murder_room)

        cards_info_new = dynamic_cards_info[:18]

        for i in range(len(cards_info_new) - 1, 0, -1):
            j = self.random.randint(0, i)
            cards_info_new[i], cards_info_new[j] = cards_info_new[j], cards_info_new[i]

        for i in range(len(cards_info_new)):
            self.all_of_cards_list[i] = Cards(cards_info_new[i % 18])

        for i in range(len(self.string_based_18_cards)):
            self.string_based_18_cards[i] = str(self.all_of_cards_list[i])

    def set_murderer_char(self, murderer_char: str):
        self.murderer_char = self.rand_select_murderer()

    def set_murder_tool(self, murder_tool: str):
        self.murder_tool = self.rand_select_murder_tool()

    def set_murder_room(self, murder_room: str):
        self.murder_room = self.rand_select_murder_room()

    def get_murderer_char(self) -> str:
        return self.murderer_char

    def get_murder_tool(self) -> str:
        return self.murder_tool

    def get_murder_room(self) -> str:
        return self.murder_room

    def get_string_based_18_cards(self) -> str:
        if self.current_card < len(self.string_based_18_cards):
            card = self.string_based_18_cards[self.current_card]
            self.current_card += 1
            return card
        else:
            return " "

    def shuffle_char_cards(self):
        characters_array_of_names = self.characters_array_of_names.copy()
        for i in range(len(characters_array_of_names) - 1, 0, -1):
            j = self.random.randint(0, i)
            characters_array_of_names[i], characters_array_of_names[j] = characters_array_of_names[j], characters_array_of_names[i]

    def shuffle_tool_cards(self):
        tools_array_of_names = self.tools_array_of_names.copy()
        for i in range(len(tools_array_of_names) - 1, 0, -1):
            j = self.random.randint(0, i)
            tools_array_of_names[i], tools_array_of_names[j] = tools_array_of_names[j], tools_array_of_names[i]

    def shuffle_room_cards(self):
        rooms_array_of_names = self.rooms_array_of_names.copy()
        for i in range(len(rooms_array_of_names) - 1, 0, -1):
            j = self.random.randint(0, i)
            rooms_array_of_names[i], rooms_array_of_names[j] = rooms_array_of_names[j], rooms_array_of_names[i]

    def rand_select_murderer(self) -> str:
        return self.random.choice(self.characters_array_of_names)

    def rand_select_murder_tool(self) -> str:
        return self.random.choice(self.tools_array_of_names)

    def rand_select_murder_room(self) -> str:
        return self.random.choice(self.rooms_array_of_names)

    def random_murder_setting_select(self, given_deck_of_cards: List[str]) -> str:
        return self.random.choice(given_deck_of_cards)

    def dealing_cards(self) -> Cards:
        if self.current_card < len(self.all_of_cards_list):
            card = self.all_of_cards_list[self.current_card]
            self.current_card += 1
            return card
        else:
            return Cards(" ")

class MainClass:
    cards_total_num = 21
    random = random.SystemRandom()
    dice1, dice2, result_of_dice = 0, 0, 0
    characters_array_of_names = ["Dr.Orchid", "Mr.Green", "Col.Mustard", "Ms.Peacock", "Prof.Plum", "Mr.Scarlet"]
    tools_array_of_names = ["wrench", "rope", "steel bar", "knife", "shovel", "razor"]
    rooms_array_of_names = ["piano room", "greenhouse", "billiard's room", "library", "study room", "hall", "bedroom", "dining", "kitchen"]
    rooms_string_and_int_map = {
        1: "hall", 2: "piano room", 3: "greenhouse", 4: "study room", 5: "billiard's room",
        6: "bedroom", 7: "dining", 8: "library", 9: "kitchen"
    }

    @staticmethod
    def main():
        print("\n\t\t\tWelcome to the 'Clue' game\n first enter the number of the players :")
        participants_total_num = int(input())
        print("**Disclaimer : due to some issues, you will always play as player1.**")

        my_deck = DeckOfCardsTotal()
        my_deck.shuffle_char_cards()
        my_deck.shuffle_tool_cards()
        my_deck.shuffle_room_cards()

        correct_answer = [my_deck.get_murderer_char(), my_deck.get_murder_tool(), my_deck.get_murder_room()]
        my_deck.shuffle_array_size_18()

        string_array_of_cards = [my_deck.get_string_based_18_cards() for _ in range(18)]

        if participants_total_num == 3:
            player1_cards = string_array_of_cards[:6]
            player2_cards = string_array_of_cards[6:12]
            player3_cards = string_array_of_cards[12:18]

            starting_room_player1 = MainClass.random.randint(1, 9)
            starting_room_player2 = MainClass.random.randint(1, 9)
            starting_room_player3 = MainClass.random.randint(1, 9)

            print(f"Player1's starting room is : {starting_room_player1}")
            print(f"Player2's starting room is : {starting_room_player2}")
            print(f"Player3's starting room is : {starting_room_player3}")

            end_of_game = False
            while not end_of_game:
                print("Player1's turn : rolling dice")
                MainClass.dice1 = MainClass.random.randint(1, 6)
                MainClass.dice2 = MainClass.random.randint(1, 6)
                MainClass.result_of_dice = (MainClass.dice1 + MainClass.dice2) % 2
                print("odd number" if MainClass.result_of_dice == 1 else "even number")

                new_room_player1 = 0
                if MainClass.result_of_dice == 1:
                    new_room_player1 = MainClass.get_new_room(starting_room_player1, [3, 5, 7, 9])
                else:
                    new_room_player1 = MainClass.get_new_room(starting_room_player1, [2, 4, 6, 8])

                starting_room_player1 = new_room_player1

                print(f"These are player1's cards (yours) : {player1_cards}\n\t**you might want to write them down**")

                gauss_for_player1_char = input("Your possible suspect's name? ")
                gauss_for_player1_tool = input("Your possible tool of murder? ")

                print("\tasking now begins...")
                asking_con = True
                while asking_con:
                    for card in player2_cards:
                        if gauss_for_player1_char in card or gauss_for_player1_tool in card:
                            print(f"player2 has the {card}'s card.")
                            asking_con = False
                            break
                    if not asking_con:
                        break
                    for card in player3_cards:
                        if gauss_for_player1_char in card or gauss_for_player1_tool in card:
                            print(f"player3 has the {card}'s card.")
                            asking_con = False
                            break
                    asking_con = False

                player1_decision = int(input("Would you like to pass(1) or make a final accusation(2)? (enter one of these numbers)"))
                if player1_decision == 2:
                    gauss_for_player1_room = MainClass.rooms_string_and_int_map[starting_room_player1]
                    accusation_for_player1 = [gauss_for_player1_char, gauss_for_player1_tool, gauss_for_player1_room]
                    if accusation_for_player1 == correct_answer:
                        print("Player1 (you) has guessed right and won! ")
                        end_of_game = True
                    else:
                        print("Player1 (you) has guessed wrong and lost...GAME OVER!")
                        end_of_game = True

                # Player2 and Player3 turns would follow similarly
                # Not finished yet

    @staticmethod
    def get_new_room(current_room: int, possible_rooms: List[int]) -> int:
        print(f"select from these options as rooms -> {possible_rooms}")
        return int(input())

if __name__ == "__main__":
    MainClass.main()