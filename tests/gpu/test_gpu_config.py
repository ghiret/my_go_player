import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "src" / "misc" / "validate_gpu_config.py"


@pytest.mark.skipif(shutil.which("nvidia-smi") is None, reason="No NVIDIA GPU; GPU checks run locally only.")
def test_all_frameworks_use_gpu():
    """TensorFlow, PyTorch, JAX and Keras on every backend must run on the local CUDA GPU."""
    result = subprocess.run([sys.executable, str(SCRIPT), "--require-gpu"], capture_output=True, text=True, timeout=600, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
