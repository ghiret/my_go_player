# Getting Started

This guide will help you set up and start using the Deep Learning and Go Project.

## Prerequisites

- Python 3.11 or higher
- Git
- uv (for dependency management)

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/ghiret/my_go_player.git
   cd my_go_player
   ```

2. Install dependencies using [uv](https://github.com/astral-sh/uv):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   sudo mv ~/.local/bin/uv /usr/local/bin/uv  # optional if not already in PATH
   uv pip install ".[dev]"
   ```

3. (Optional) If you're on **Apple Silicon (macOS)** and need GPU support:
   ```bash
   python3.11 -m venv venv311
   source venv311/bin/activate
   uv pip install ".[dev]"
   python src/misc/validate_gpu_config.py
   ```

4. (Optional) On **Linux with CUDA** (e.g., Ubuntu + NVIDIA GPU):
   ```bash
   # If inside devcontainer, activate its venv
   source /home/ubuntu/venv/bin/activate

   # If running locally:
   python3.11 -m venv .venv
   source .venv/bin/activate

   uv pip install ".[dev]"
   python src/misc/validate_gpu_config.py
   ```

## ✅ Verifying Installation

To ensure everything is working, run the unit tests:

```bash
pytest
```

## Next Steps

Now that you have the project set up, you can explore the different components:

- Check out the [Chapter 6 Guide](chapter6.md) to start developing a machine learning application for Go.
- Move on to the [Chapter 7 Guide](chapter7.md) to learn about processing and learning from Go game data.

For more detailed information about the project structure and components, refer to the [About](about.md) page.
