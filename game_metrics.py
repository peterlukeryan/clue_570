import random
from time import time
import matplotlib.pyplot as plt


class Metrics:
    def __init__(self):
        self.turns = []
        self.accusations = []
        self.wins = []
        self.bluffs = []
        self.start_time = None
        self.end_time = None

    def start_timer(self):
        self.start_time = time()

    def end_timer(self):
        self.end_time = time()

    def record_turn(self, duration):
        self.turns.append(duration)

    def record_accusation(self, player, is_bluff=False):
        self.accusations.append(player)
        if is_bluff:
            self.bluffs.append((player, len(self.turns) + 1))

    def record_win(self, player):
        self.wins.append((player, len(self.turns)))

    def print_metrics(self):
        total_time = self.end_time - self.start_time if self.start_time and self.end_time else 0
        average_turn_duration = sum(self.turns) / len(self.turns) if self.turns else 0
        print("Game Metrics Summary:")
        print(f"Total Game Time: {total_time:.2f} seconds")
        print(f"Total Turns: {len(self.turns)}")
        print(f"Average Turn Duration: {average_turn_duration:.2f} seconds")
        print(f"Total Accusations Made: {len(self.accusations)}")
        print(f"Bluffs Detected: {len(self.bluffs)}")

    def plot_metrics(self):
        win_turns = [win[1] for win in self.wins]
        plt.figure(figsize=(10, 5))
        plt.hist(win_turns, bins=range(1, len(self.turns) + 2), edgecolor="black", color="skyblue", alpha=0.7)
        plt.title("Wins Over Time")
        plt.xlabel("Turn Number")
        plt.ylabel("Wins")
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.plot(range(1, len(self.accusations) + 1), range(1, len(self.accusations) + 1), marker="o", color="orange")
        plt.title("Accusations Over Time")
        plt.xlabel("Accusation Number")
        plt.ylabel("Number of Accusations")
        plt.show()

        bluff_count = len(self.bluffs)
        non_bluff_count = len(self.accusations) - bluff_count
        plt.figure(figsize=(5, 5))
        plt.pie([bluff_count, non_bluff_count], labels=["Bluff", "Non-Bluff"], autopct="%1.1f%%", startangle=90,
                colors=["red", "green"])
        plt.title("Bluffing vs. Non-Bluffing")
        plt.show()
