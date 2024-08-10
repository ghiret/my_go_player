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
