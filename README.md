# Grid World Reinforcement Learning

This project implements a grid world environment for RL, where an agent (naruto) learns to navigate a grid to reach a target (sasuke). The environment and agent are built using the `gymnasium` library and `pygame` for rendering.

## Components

- **GridWorldEnv**: A custom environment that simulates a grid world. It includes a player and a target, both represented as sprites. The environment supports different rendering modes and provides observations and rewards to the agent.

- **GridWorldAgent**: An agent that interacts with the grid world environment using Q-learning. It learns optimal actions to maximise rewards by exploring and exploiting the environment.

- **Player and Target**: These are sprite classes representing the player and the target within the grid. They are responsible for loading and scaling images to fit the grid cells.

- **GridCell**: Represents individual cells in the grid, forming the environment's layout.

## Features

- **Q-Learning**: The agent uses Q-learning,

- **Exploration and Exploitation**: The agent balances exploration and exploitation using an epsilon-greedy strategy, with epsilon decaying over time to favour exploitation.

- **Visualisation**: The environment can be rendered using `pygame`, allowing for visualisation of the agent's learning process.
  
![naruto_sasuke_gif](https://github.com/user-attachments/assets/b39cc464-b1ac-44e6-a6ff-ed16f0be952b)
