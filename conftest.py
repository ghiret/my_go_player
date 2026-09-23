import os
import sys
from pathlib import Path

# Get the project root directory
root_dir = Path(__file__).parent

# Add the project root and src directories to Python path
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "src"))
sys.path.insert(0, str(root_dir / "tests"))

print("Python path in conftest:", sys.path)

# Allocate GPU memory on demand instead of grabbing it all at start-up, so several
# frameworks (and the GPU validation subprocesses) can share a small local GPU.
os.environ.setdefault("TF_FORCE_GPU_ALLOW_GROWTH", "true")
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
