import tensorflow as tf


def validate_gpu():
    print("TensorFlow version:", tf.__version__)

    # Check for available GPUs
    physical_devices = tf.config.list_physical_devices()
    print("Available physical devices:")
    for device in physical_devices:
        print(f"  {device.device_type}: {device.name}")

    gpus = tf.config.list_physical_devices("GPU")
    if gpus:
        print(f"\nNumber of GPUs available: {len(gpus)}")
        for gpu in gpus:
            print(f"  {gpu.name}")

        # Try to create a simple TensorFlow operation on the GPU
        try:
            with tf.device("/GPU:0"):
                a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
                b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
                c = tf.matmul(a, b)
            print("\nSuccessfully performed a GPU operation.")
            print("Result:", c.numpy())
        except RuntimeError as e:
            print("\nFailed to perform GPU operation:", str(e))
    else:
        print("\nNo GPUs found. TensorFlow will use CPU.")

    # Check if TensorFlow is using Metal
    if tf.test.is_built_with_cuda():
        print("\nTensorFlow is built with CUDA support (for NVIDIA GPUs).")
    elif len(gpus) > 0:
        print("\nTensorFlow is likely using Metal (Apple GPU).")
    else:
        print("\nTensorFlow is using CPU only.")


if __name__ == "__main__":
    validate_gpu()
