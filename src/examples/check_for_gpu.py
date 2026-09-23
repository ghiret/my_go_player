import keras


def check_gpu_availability():
    """Report the GPUs visible to the active Keras backend (set via KERAS_BACKEND)."""
    backend = keras.backend.backend()
    print("Keras version:", keras.__version__, "| backend:", backend)

    if backend == "jax":
        import jax

        print("JAX version:", jax.__version__)
        print("Devices:", jax.devices())
        gpus = [d for d in jax.devices() if d.platform == "gpu"]
    elif backend == "tensorflow":
        import tensorflow as tf

        print("TensorFlow version:", tf.__version__)
        print("Devices:", tf.config.list_physical_devices())
        gpus = tf.config.list_physical_devices("GPU")
    elif backend == "torch":
        import torch

        print("PyTorch version:", torch.__version__)
        gpus = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
    else:
        gpus = []

    print("Num GPUs Available:", len(gpus))
    if not gpus:
        print("No GPU found. Using CPU.")
    return len(gpus)
