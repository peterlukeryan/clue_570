import random
import numpy as np
from Player import Player

class RLPlayer(Player):
    def __init__(self, player_id=None, player_map=None, alpha=0.1, gamma=0.9, epsilon=0.1):
        super().__init__(player_id, player_map)
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = {}  # Q-table to store state-action values

    def get_state(self):
        #Convert the current state into a hashable format.
        return (str(self.suspects[0]), str(self.suspects[1]), str(self.suspects[2]))

    def choose_action(self, state):
        # Epsilon-greedy policy.
        
        if random.uniform(0, 1) < self.epsilon:
            # Explore: choose a random action
            return random.choice(self.get_possible_actions())
        else:
            # Exploit: choose the best known action
            return self.get_best_action(state)

    def get_possible_actions(self):
        return ["reveal", "accuse"]

    def get_best_action(self, state):
        # action with highest Q-value for the given state.
        if state not in self.q_table:
            self.q_table[state] = {action: 0 for action in self.get_possible_actions()}
        return max(self.q_table[state], key=self.q_table[state].get)

    def update_q_table(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {action: 0 for action in self.get_possible_actions()}
        if next_state not in self.q_table:
            self.q_table[next_state] = {action: 0 for action in self.get_possible_actions()}

        old_value = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values())

        # Q-learning formula ??? 
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[state][action] = new_value

    def calculate_reward(self, action, is_correct_accusation):
        # This could be messed up. I'm guessing here
        if action == "accuse":
            if is_correct_accusation:
                return 10  
            else:
                return -5  
        elif action == "reveal":
            return -1  # Small penalty for revealing cards
        return 0  # Default reward

    def reveal_cards(self):
        state = self.get_state()
        action = self.choose_action(state)

        # Simulate revealing cards placeholder
        # This will need to be fixed ?
        print(f"Player {self.player_id} is revealing cards.")
        reward = self.calculate_reward(action, None)  # No outcome for revealing
        next_state = self.get_state()

        # Update the Q-table
        self.update_q_table(state, action, reward, next_state)

    def make_accusation(self, players, turn, num_players):
        """
        Override the make_accusation method to include RL logic.
        """
        state = self.get_state()
        action = self.choose_action(state)

        if action == "accuse":
            # Make an accusation using the parent class's logic
            # I don't think this is what we're supposed to be doing
            # Or is it?
            is_correct = super().make_accusation(players, turn, num_players)
            reward = self.calculate_reward(action, is_correct)
            next_state = self.get_state()

            # Update the Q-table
            self.update_q_table(state, action, reward, next_state)

            # Return whether the game is over
            return is_correct
        else:
            # If not accusing, proceed with normal logic
            return super().make_accusation(players, turn, num_players)

    # Retain all other methods from the Player class
    def respond(self, cards):
        """
        Respond to an accusation by another player.
        """
        for card in cards:
            if card in self.player_map[self.player_id]:
                return card
        return None

    def show_hand(self):
        """
        Show the player's hand.
        """
        return f"Player's hand: {self.player_map[self.player_id]}"

    def show_suspect_list(self):
        """
        Show the player's suspect list.
        """
        return f"Suspect list: {self.suspects}"

    def accuse(self, player, cards):
        """
        Accuse another player of having specific cards.
        """
        return player.respond(cards)