# Chapter 7: Learning from Data

This guide covers the code and concepts related to Chapter 7 of "Deep Learning and the Game of Go," focusing on generating and processing game data.

## Generating MCTS Game Data

To generate game data using Monte Carlo Tree Search (MCTS):

```bash
poetry run python src/scripts/generate_mcts_games.py -n 20 --board-out features.npy --move-out labels.npy -b 5
```

This command:
- Generates 20 games (`-n 20`)
- Saves board positions to `features.npy`
- Saves corresponding moves to `labels.npy`
- Uses a 5x5 board (`-b 5`)

You can adjust these parameters as needed.

## Understanding the Generated Data

- `features.npy`: Contains the board positions (features) for each move.
- `labels.npy`: Contains the corresponding moves (labels) made by the MCTS bot.

This data can be used to train machine learning models to predict moves based on board positions.

## Next Steps

After generating the data:
1. Explore the generated `.npy` files using numpy to understand their structure.
2. Use this data to train a neural network model (covered in later chapters).

## Key Components

- `src/scripts/generate_mcts_games.py`: The main script for generating game data.
- `src/bots/mcts_bot.py`: Implements the Monte Carlo Tree Search bot.

Dive into these files to understand how MCTS works and how the game data is generated and structured.
