# About Deep Learning and Go Project

## Project Background

This project is a personal implementation and exploration of the concepts presented in the book "Deep Learning and the Game of Go" by Max Pumperla and Kevin Ferguson. It serves as an educational journey into the intersection of artificial intelligence, deep learning, and the ancient game of Go.

## Motivation

The primary motivation behind this project is to gain a comprehensive understanding of how modern AI techniques can be applied to complex strategic games like Go. By implementing the algorithms and models described in the book, we aim to:

1. Deepen our understanding of deep learning concepts
2. Explore the intricacies of the game of Go from a computational perspective
3. Gain practical experience in implementing and testing AI models

## Key Features

- Implementation of various Go-playing bots, including random and MCTS-based players
- Tools for generating and processing game data
- Integration with deep learning frameworks for model training and evaluation
- Comprehensive unit testing suite

## Technical Stack

- **Programming Language**: Python
- **Deep Learning Framework**: TensorFlow (with potential future ports to PyTorch)
- **Testing Framework**: pytest
- **Package Management**: Poetry
- **Version Control**: Git
- **Continuous Integration**: GitHub Actions
- **Code Coverage**: Codecov.io

## Project Structure

The project is organized into several key components:

1. **Core Go Logic**: Implementation of Go game rules and board representation
2. **AI Players**: Various bot implementations, from simple random players to more advanced MCTS-based ones
3. **Data Generation**: Scripts and tools for creating training datasets
4. **Model Training**: Implementation of deep learning models for Go strategy
5. **Evaluation**: Tools for assessing the performance of different AI players

## Development Approach

Our development process is iterative and focused on learning:

1. Study and understand concepts from the book
2. Implement core functionality based on book examples
3. Refactor and optimize code for clarity and performance
4. Add comprehensive unit tests, often generated with AI assistance
5. Continuously integrate new learnings and improvements

## AI-Assisted Development

A unique aspect of this project is the integration of AI in the development process itself:

- Many unit tests are initially generated using Large Language Models (LLMs) like Claude 3.5 Sonnet and GPT-4
- These AI-generated tests are carefully reviewed, modified, and integrated into the project
- This approach allows for rapid development of a comprehensive test suite while also serving as a learning tool

## Code Coverage

We use Codecov.io to measure and track code coverage. You can view the current coverage status and detailed reports at:

[https://app.codecov.io/gh/ghiret/my_go_player](https://app.codecov.io/gh/ghiret/my_go_player)

## Acknowledgements

We extend our gratitude to Max Pumperla and Kevin Ferguson for their excellent book "Deep Learning and the Game of Go," which serves as the foundation for this project. Their work has made complex AI concepts accessible and applicable to this fascinating domain.