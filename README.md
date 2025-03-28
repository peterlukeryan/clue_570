# Clue Bluffing Study

Project for CSC 570-- Rodrigo Canaan-- Cal Poly (Anthony H. Navya M. Sophie R. Peter R. Ramon T.) Special thanks to OpenAI's Gymnasium docs for tutorials on implementing
RL agents, as well as David and Kyle Hansen for their work on the theoritcal soundness of bluffing in Clue.
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
WARNING the agent trained below is massive. Training takes upwards of two hours on a 2017 Macbook Pro, and the downloaded Q table will drain system
resources. If you would like to run a less demanding model, we suggest adjusting the num_episodes hyperparameter to 100_000. However, since 1_000_000
was used in the report, I have left it as is.
* Run `EpsilonDeltaAgent.py` to train the model. This will print upon success: *Training complete. Model saved as trained_model.pkl.* 
* Run `EpsilonDeltaAgent.py` to play with agent (One RL Agent, Five regular bots)


### Files
* `EpsilonDeltaAgent.py` is the logic used to train our first RL Clue playing agent 
* `Epsilon_agent_trained.py` is a file where the epsilon greedy agent can be tested

### Replicating results
* Our main result for the deduction bot is built into clue_testbed.py. A printout is executed representing a dictionary in which
  the keys are the player index and the values are the win counts. Player 0 represents the deduction agent.



## Notes
Several dependencies are required– Open AI’s “gym”, numpy and pickle (virtual environment is recommended for use)





## Authors
Anthony Herrera, Navya Mishra, Sophie Russ, Peter Ryan, and Ramon Torres
