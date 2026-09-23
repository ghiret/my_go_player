"""Validate that TensorFlow, PyTorch, JAX and Keras 3 (on every backend) can see the GPU.

Usage:
    python src/misc/validate_gpu_config.py            # check everything
    python src/misc/validate_gpu_config.py --require-gpu   # exit non-zero if any check falls back to CPU

Keras fixes its backend at import time, so each Keras backend is checked in a
separate subprocess with ``KERAS_BACKEND`` set.
"""

import argparse
import os
import subprocess
import sys

KERAS_BACKENDS = ("jax", "tensorflow", "torch")


def check_tensorflow():
    import tensorflow as tf

    print("TensorFlow version:", tf.__version__)
    gpus = tf.config.list_physical_devices("GPU")
    print("  Built with CUDA:", tf.test.is_built_with_cuda())
    print("  GPUs:", [gpu.name for gpu in gpus])
    if not gpus:
        return False
    with tf.device("/GPU:0"):
        c = tf.matmul(tf.ones((2, 3)), tf.ones((3, 2)))
    print("  matmul on", c.device)
    return True


def check_torch():
    import torch

    print("PyTorch version:", torch.__version__)
    if torch.cuda.is_available():
        print("  CUDA version:", torch.version.cuda, "| device:", torch.cuda.get_device_name(0))
        device = "cuda"
    elif torch.backends.mps.is_available():
        print("  Apple MPS available")
        device = "mps"
    else:
        print("  No GPU available")
        return False
    c = torch.ones((2, 3), device=device) @ torch.ones((3, 2), device=device)
    print("  matmul on", c.device)
    return True


def check_jax():
    import jax
    import jax.numpy as jnp

    print("JAX version:", jax.__version__)
    print("  Default backend:", jax.default_backend())
    print("  Devices:", jax.devices())
    c = jnp.ones((2, 3)) @ jnp.ones((3, 2))
    print("  matmul on", c.devices())
    return jax.default_backend() == "gpu"


def check_keras():
    """Train one tiny Conv2D model step with the backend selected via KERAS_BACKEND."""
    import keras
    import numpy as np

    backend = keras.backend.backend()
    print(f"Keras {keras.__version__} with backend '{backend}'")
    model = keras.Sequential(
        [
            keras.Input(shape=(9, 9, 1)),
            keras.layers.Conv2D(8, (3, 3), padding="same", activation="relu"),
            keras.layers.Flatten(),
            keras.layers.Dense(81, activation="softmax"),
        ]
    )
    model.compile(loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])
    x = np.random.rand(32, 9, 9, 1).astype("float32")
    y = keras.utils.to_categorical(np.random.randint(0, 81, 32), 81)
    model.fit(x, y, epochs=1, batch_size=16, verbose=0)

    if backend == "jax":
        import jax

        on_gpu = jax.default_backend() == "gpu"
    elif backend == "tensorflow":
        import tensorflow as tf

        on_gpu = bool(tf.config.list_physical_devices("GPU"))
    else:
        import torch

        on_gpu = torch.cuda.is_available() or torch.backends.mps.is_available()
    print("  Trained one epoch on", "GPU" if on_gpu else "CPU")
    return on_gpu


def run_keras_backend(backend):
    sys.stdout.flush()
    env = {**os.environ, "KERAS_BACKEND": backend, "TF_CPP_MIN_LOG_LEVEL": "2"}
    result = subprocess.run([sys.executable, __file__, "--keras-only"], env=env, check=False)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--require-gpu", action="store_true", help="Fail if any framework runs on CPU.")
    parser.add_argument("--keras-only", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.keras_only:
        sys.exit(0 if check_keras() else 1)

    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
    results = {}
    for name, check in (("tensorflow", check_tensorflow), ("torch", check_torch), ("jax", check_jax)):
        try:
            results[name] = check()
        except Exception as e:  # noqa: BLE001 - report and continue with the other frameworks
            print(f"  {name} check failed: {e}")
            results[name] = False
        print()

    for backend in KERAS_BACKENDS:
        results[f"keras[{backend}]"] = run_keras_backend(backend)
        print()

    print("Summary:")
    for name, on_gpu in results.items():
        print(f"  {name:20s} {'GPU' if on_gpu else 'CPU / unavailable'}")

    if args.require_gpu and not all(results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
