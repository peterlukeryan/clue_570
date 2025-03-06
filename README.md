# Clue Bluffing Study

This repository contains a Clue simulation. We employ reinforcement learning techniques to analyze the strategy of bluffing. 


## Installation 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install gym.

```bash
pip install gym
```

## Usage

The file `clue_testbed.py` is the main file used to demo all agents. This file has an **Deduction Agent** which uses an advanced Clue strategy to play against **Regular Bot** which uses the standard "elimination" strategy (Hansen et al.). 

The game is modeled using 'Players' which are objects with typical properties (e.g. hand, suspect list, a player map). The player map is a dictionary representing other players' information. 

The game of Clue has  been treated as a problem in which players reduce their "suspect list" (e.g. who could possibly have committed the murder by accusing players according to the rules of Clue). 

Currently, there are no heuristics in the responses to accusations (the first matching card is discarded)-- although this is a potential area to explore.

### RL Agent
Run `EpsilonDeltaAgent.py` to train the model 
Completion message: “Training complete. Model saved as trained_model.pkl.”

Run `EpsilonDeltaAgent.py` to play with agent (One RL Agent, Five regular bots)


### Files
`EpsilonDeltaAgent.py` is the logic used to train our first RL Clue playing agent
`Epsilon_agent_trained.py` is a file where the epsilon greedy agent can be tested



## Notes
Several dependencies are required– Open AI’s “gym”, numpy and pickle (virtual environment is recommended for use)





## Authors
Anthony Herrera, Navya Mishra, Sophie Russ, Peter Ryan, and Ramon Torres
