Clue Bluffing Experiment--

This repo contains a Clue simulation in which we attempt to apply Reinforcement Learning to analyze the strategy of bluffing. 
Currently, the file clue_testbed.py is where we are experimenting with our agents. The game is modeled using "Players"
i.e objects with "typical" properties like hand, suspect list and a "player map" which is a dictionary representing other
players' information. The game of Clue has essentially been treated as a problem in which players reduce their "suspect list"--
i.e who could possibly have commited the murder by accusing players according to the rules of Clue. Currently, there are no heuristics 
in the responses to accusations (the first matching card is discarded)-- although this is a potential area to explore.
