[![codecov](https://codecov.io/gh/ghiret/my_go_player/graph/badge.svg?token=GURIMLWFMA)](https://codecov.io/gh/ghiret/my_go_player)
# my_go_player
# Deep Learning and Go Project

## Project Overview

This project is a personal implementation and exploration of the concepts presented in the book "Deep Learning and the Game of Go" by Max Pumperla and Kevin Ferguson. It serves as a learning exercise and a practical application of the ideas discussed in the book.

## Origin and Inspiration

- **Book**: [Deep Learning and the Game of Go](https://www.manning.com/books/deep-learning-and-the-game-of-go) by Max Pumperla and Kevin Ferguson, published by Manning Publications.
- **Original Repository**: [deep_learning_and_the_game_of_go](https://github.com/maxpumperla/deep_learning_and_the_game_of_go)

## Project Purpose

The primary goals of this project are:

1. To gain a deep understanding of the concepts presented in the book.
2. To practice implementing machine learning algorithms in the context of the game of Go.
3. To explore software development practices, including unit testing and code organization.

## Development Approach

The development process for this project follows these steps:

1. Reading and studying the relevant chapters of the book.
2. Implementing the code based on the book's examples and the original GitHub repository.
3. Refactoring and adjusting the code as needed for better understanding or performance.
4. Adding comprehensive unit tests to ensure code correctness and to deepen understanding of the implemented concepts.

## Unit Testing

- Unit tests are an integral part of this project, serving both as a verification tool and a learning aid.
- The majority of the unit tests are generated using Large Language Models (LLMs), primarily Claude 3.5 Sonnet and occasionally GPT-4.
- These AI-generated tests are then reviewed, modified as necessary, and integrated into the project.

## Licensing and Attribution

As of the creation of this project, the original book and GitHub repository do not specify a license. This project is created for educational purposes and is not intended for commercial use. All credit for the original concepts, algorithms, and code structure goes to the authors of "Deep Learning and the Game of Go."

If you intend to use any part of this code, please refer to the original book and repository, and be aware of potential copyright considerations.

## Disclaimer

This is not an official implementation of the book's code. It is a personal project created for learning purposes. There may be differences from the original implementation due to personal interpretation, updates, or improvements made during the learning process.

## Contributions

While this is primarily a personal learning project, observations, suggestions, or discussions about the implementations and concepts are welcome. Please open an issue in the repository if you'd like to discuss any aspect of the project.

## Acknowledgements

Special thanks to Max Pumperla and Kevin Ferguson for writing "Deep Learning and the Game of Go," which serves as the foundation and inspiration for this project.
### How to play random bot vs random bot

```bash
poetry run python src/scripts/random_bot_vs_random_bot.py
```

### How to play against the random bot

```bash
poetry run python src/scripts/human_vs_random_bot.py
```

### How to generate mcts data
```bash
 poetry run python src/scripts/generate_mcts_games.py -n 20 --board-out features.npy --move-out labels.npy -b 5
```

### Configuring the gpu for Apple sillicon
I have not been able to get the GPUs working with devcontainer, so I am resorting to a python virtual environment.
```bash
python3.11 -m venv venv311
source venv311/bin/activate
poetry install
poetry run python src/misc/validate_gpu_config.py
```
