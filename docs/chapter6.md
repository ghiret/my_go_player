# Chapter 6: Developing a Machine Learning Application

This guide covers the code and concepts related to Chapter 6 of "Deep Learning and the Game of Go."

## Running a Game: Random Bot vs Random Bot

To simulate a game between two random bots:

```bash
poetry run python src/scripts/random_bot_vs_random_bot.py
```

This script demonstrates the basic game mechanics and how simple AI players make moves.

## Playing Against the Random Bot

To play a game against the random bot:

```bash
poetry run python src/scripts/human_vs_random_bot.py
```

This interactive script allows you to play against a bot that makes random moves, helping you understand the game flow and bot interaction.

## Understanding the Code

These scripts utilize the core game logic and the random bot implementation. Key components include:

- `src/go_engine/`: Contains the core Go game logic.
- `src/bots/random_bot.py`: Implements the random bot player.

Explore these files to understand how the game state is managed and how the random bot makes decisions.
