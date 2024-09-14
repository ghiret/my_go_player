import tensorflow as tf
from keras.layers import Conv2D, Flatten  # <1>


def check_gpu_availability():

    print("TensorFlow version:", tf.__version__)
    print("Num GPUs Available: ", len(tf.config.list_physical_devices("GPU")))
    print("Devices:", tf.config.list_physical_devices())

    try:
        tf.config.experimental.set_visible_devices(tf.config.list_physical_devices("GPU")[0], "GPU")
        logical_gpus = tf.config.experimental.list_logical_devices("GPU")
        print(len(logical_gpus), "Logical GPU(s) found")
    except:
        print("No GPU found. Using CPU.")
