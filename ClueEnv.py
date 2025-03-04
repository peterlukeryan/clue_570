import gym
import random
from gym import spaces
from Player import Player

class ClueEnv(gym.Env):
    def __init__(self, num_players=6):
        super(ClueEnv, self).__init__()

        self.characters = ["Dr. Orchid", "Mr. Green", "Col. Mustard", "Ms. Peacock", "Prof. Plum", "Ms. Scarlett"]
        self.weapons = ["Wrench", "Rope", "Steel Bar", "Knife", "Shovel", "Razor"]
        self.rooms = ["Hall", "Piano Room", "Greenhouse", "Study", "Billiard Room", "Bedroom", "Dining Room", "Library",
                      "Kitchen"]
        self.all_cards = self.characters + self.weapons + self.rooms

        self.num_players = num_players
        self.game_over = False
        self.action_space = spaces.Tuple((
            spaces.Discrete(len(self.characters)),
            spaces.Discrete(len(self.weapons)),
            spaces.Discrete(len(self.rooms)),
            spaces.Discrete(2)
        ))

        self.observation_space = spaces.Tuple((
            spaces.Discrete(len(self.characters) + len(self.weapons) + len(self.rooms)),
            spaces.Discrete(self.num_players)
        ))

        self.reset()

    def reset(self):
        self.murder_character = random.choice(self.characters)
        self.murder_weapon = random.choice(self.weapons)
        self.murder_room = random.choice(self.rooms)
        self.murder_cards = [self.murder_character, self.murder_weapon, self.murder_room]
        self.game_over = False
        #print("Murder scenario: " + self.murder_character + " with the " + self.murder_weapon + " in the " + self.murder_room)

        new_characters = [c for c in self.characters if c != self.murder_character]
        new_weapons = [w for w in self.weapons if w != self.murder_weapon]
        new_rooms = [r for r in self.rooms if r != self.murder_room]

        pooled_cards = new_characters + new_weapons + new_rooms

        random.shuffle(pooled_cards)

        num_players = self.num_players  # can modify however
        hands = [pooled_cards[i::num_players] for i in range(num_players)]  # Distribute cards evenly

        players = []
        for i in range(num_players):
            cur_player_map = dict()
            for j in range(num_players):
                if j != i:
                    cur_player_map[j] = []
                else:
                    cur_player_map[j] = hands[i]

            players.append(Player(player_map=cur_player_map, player_id=i))
            players[i].initialize_suspects()

        self.players = players
        self.rl_agent = players[0]
        self.current_player = 0
        self.turn = 0
        # print("RL agent's info: ")
        # print(self.rl_agent.player_map)
        # print("Suspects")
        # print(self.rl_agent.show_suspect_list())
        return (0, 0)  # Placeholder observation

    def step(self, action):
        character_idx, weapon_idx, room_idx, is_final = action

        character = self.characters[character_idx]
        weapon = self.weapons[weapon_idx]
        room = self.rooms[room_idx]

        accusation = [character, weapon, room]
        #print("Agent's accusation: ")
        #print(accusation)

        if is_final:
            #print("RL_agent goes for it all. ")
            #print(accusation)
            # Final accusation
            if accusation == self.murder_cards:
                reward = 50  # Big reward for winning
                self.game_over = True
                done = True

            else:
                reward = -100  # Huge penalty for guessing wrong
                self.game_over = True
                done = True
            observation = (0,0)
            return observation, reward, done, {}

        else:
            # RL_Agent's turn
            accusation_index = 1
            rl_discard = ""
            while accusation_index <= self.num_players and not rl_discard:

                rl_discard = self.rl_agent.accuse(self.players[(self.turn + accusation_index) % self.num_players], accusation)
                accusation_index += 1
            if rl_discard:
                player_who_refuted_rl = (self.turn + accusation_index - 1) % self.num_players
                self.rl_agent.player_map[player_who_refuted_rl].append(rl_discard)

                if rl_discard in self.rl_agent.suspects[0]:
                    self.rl_agent.suspects[0].remove(rl_discard)
                elif rl_discard in self.rl_agent.suspects[1]:
                    self.rl_agent.suspects[1].remove(rl_discard)
                elif rl_discard in self.rl_agent.suspects[2]:
                    self.rl_agent.suspects[2].remove(rl_discard)

            for i in range(1,self.num_players):
                current_player = self.players[i]
                if len(current_player.suspects[0]) == 1 and len(current_player.suspects[1]) == 1 and len(
                        current_player.suspects[2]) == 1:
                    # ya dun lost RL_Agent :(
                    current_player.final_accusation()
                    if (current_player.final_accusation() == self.murder_cards):
                        observation = (0,0)
                        reward = -100
                        done = True
                        return observation, reward, done, {}

                # 'basic' heuristic
                accusation_cards = [current_player.suspects[0][0], current_player.suspects[1][0], current_player.suspects[2][0]]
                # print("Regular bot " + str(i) + " 's accusation")
                # print(accusation_cards)
                accusation_index = 1
                discard = ""
                while accusation_index <= self.num_players and not discard:
                    discard = current_player.accuse(self.players[(i + accusation_index) % self.num_players], accusation_cards)
                    accusation_index += 1

                if discard:
                    #print(discard)

                    player_who_refuted = (i + accusation_index - 1) % self.num_players
                    current_player.player_map[player_who_refuted].append(discard)

                    if discard in current_player.suspects[0]:
                        current_player.suspects[0].remove(discard)
                    elif discard in current_player.suspects[1]:
                        current_player.suspects[1].remove(discard)
                    else:
                        current_player.suspects[2].remove(discard)
                else:

                    current_player.final_accusation()
                    done = True
                    reward = -100
                    self.game_over = True
                    observation = (0,0)
                    return observation, reward, done, {}
            done = False
            reward = 5
            if (rl_discard):
                observation = (self.all_cards.index(rl_discard), player_who_refuted_rl)
            else:
                observation = (42, 42)
            return observation, reward, done, {}


test_env = ClueEnv(num_players= 6)

observation = test_env.reset()
print("Initial observation:", observation)

# Run a few test steps
for _ in range(100):  # Take 5 steps
    action = (
        random.randint(0, len(test_env.characters) - 1),  # Random character
        random.randint(0, len(test_env.weapons) - 1),  # Random weapon
        random.randint(0, len(test_env.rooms) - 1),  # Random room
        random.randint(0,1) # Randomly choose whether it's a final accusation
    )

    obs, reward, done, info = test_env.step(action)
    print(f"Action: {action}, Observation: {obs}, Reward: {reward}, Done: {done}")

    if done:
        print("Game Over!")
        break



