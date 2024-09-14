# Getting Started

This guide will help you set up and start using the Deep Learning and Go Project.

## Prerequisites

- Python 3.7 or higher
- Git
- Poetry (for dependency management)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ghiret/my_go_player.git
   cd my_go_player
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. (Optional) If you're using an Apple Silicon Mac and want to configure GPU support:
   ```
   python3.11 -m venv venv311
   source venv311/bin/activate
   poetry install
   poetry run python src/misc/validate_gpu_config.py
   ```

## Verifying Installation

To ensure everything is set up correctly, you can run the unit tests:

```
poetry run pytest
```

## Next Steps

Now that you have the project set up, you can explore the different components:

- Check out the [Chapter 6 Guide](chapter6.md) to start developing a machine learning application for Go.
- Move on to the [Chapter 7 Guide](chapter7.md) to learn about processing and learning from Go game data.

For more detailed information about the project structure and components, refer to the [About](about.md) page.