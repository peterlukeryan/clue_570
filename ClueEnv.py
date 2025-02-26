import numpy as np
import random
from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts

from Player import Player


class ClueEnv(py_environment.PyEnvironment):
    """A TF-Agents compatible environment for Clue."""

    def __init__(self, num_players=3):
        super().__init__()

        # Game elements
        self.characters = ["Dr. Orchid", "Mr. Green", "Col. Mustard", "Ms. Peacock", "Prof. Plum", "Ms. Scarlett"]
        self.weapons = ["Wrench", "Rope", "Steel Bar", "Knife", "Shovel", "Razor"]
        self.rooms = ["Hall", "Piano Room", "Greenhouse", "Study", "Billiard Room", "Bedroom", "Dining Room", "Library",
                      "Kitchen"]
        self.solution = None  # Murder case to be solved
        self.num_players = num_players
        self.players = []
        self.current_player_idx = 0  # Track which player's turn it is

        # Define action and observation specs
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(3,), dtype=np.int32, minimum=0, maximum=len(self.characters) - 1, name="accusation"
        )  # Action = (character, weapon, room)

        self._observation_spec = {
            "suspects": array_spec.BoundedArraySpec(
                shape=(6,), dtype=np.int32, minimum=0, maximum=1, name="suspects"
            ),
            "weapons": array_spec.BoundedArraySpec(
                shape=(6,), dtype=np.int32, minimum=0, maximum=1, name="weapons"
            ),
            "rooms": array_spec.BoundedArraySpec(
                shape=(9,), dtype=np.int32, minimum=0, maximum=1, name="rooms"
            ),
            "hand": array_spec.BoundedArraySpec(
                shape=(21,), dtype=np.int32, minimum=0, maximum=1, name="hand"
            )
        }

        self._reset()

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        """Resets the game state."""
        self._deal_cards()
        self.current_player_idx = 0  # Start from first player

        return ts.restart(self._get_observation())

    def _step(self, action):
        """Processes a player's action."""
        current_player = self.players[self.current_player_idx]
        accusation = [self.characters[action[0]], self.weapons[action[1]], self.rooms[action[2]]]

        if accusation == self.solution:
            return ts.termination(self._get_observation(), reward=10)  # Correct accusation

        # If incorrect, the player is eliminated
        return ts.transition(self._get_observation(), reward=-1, discount=0.9)

    def _deal_cards(self):
        """Distributes cards to players and sets up the game."""
        all_cards = self.characters + self.weapons + self.rooms
        random.shuffle(all_cards)

        # Choose a random solution (1 character, 1 weapon, 1 room)
        self.solution = [random.choice(self.characters), random.choice(self.weapons), random.choice(self.rooms)]
        for card in self.solution:
            all_cards.remove(card)

        # Distribute remaining cards among players
        player_map = {i: [] for i in range(self.num_players)}
        for i, card in enumerate(all_cards):
            player_map[i % self.num_players].append(card)

        # Create players
        self.players = [Player(player_id=i, player_map=player_map) for i in range(self.num_players)]
        for player in self.players:
            player.initialize_suspects()

    def _get_observation(self):
        """Encodes the observation for the current player."""
        player = self.players[self.current_player_idx]
        suspect_encoding = np.zeros((3, 6), dtype=np.int32)

        # Encode suspects (1 if the player still suspects it, 0 if eliminated)
        for i, category in enumerate(player.suspects):
            for suspect in category:
                idx = self.characters.index(suspect) if i == 0 else self.weapons.index(
                    suspect) if i == 1 else self.rooms.index(suspect)
                suspect_encoding[i, idx] = 1

        # Encode the player's hand
        hand_encoding = np.zeros(6, dtype=np.int32)
        for card in player.player_map[player.player_id]:
            idx = self.characters.index(card) if card in self.characters else self.weapons.index(
                card) if card in self.weapons else self.rooms.index(card)
            hand_encoding[idx] = 1

        return {"suspects": suspect_encoding, "hand": hand_encoding}
