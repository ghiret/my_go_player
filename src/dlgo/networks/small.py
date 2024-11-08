# Copied from https://github.com/maxpumperla/deep_learning_and_the_game_of_go/blob/master/code/dlgo/networks/small.py
from __future__ import absolute_import

import keras
from keras.layers import Activation, Conv2D, Dense, Flatten, Input, ZeroPadding2D


def layers(input_shape):
    return [
        # Add an Input layer to specify the input shape
        Input(shape=input_shape),
        # We use zero padding layers to enlarge input images.
        ZeroPadding2D(padding=3, data_format="channels_last"),
        Conv2D(48, (7, 7), data_format="channels_last"),
        Activation("relu"),
        ZeroPadding2D(padding=2, data_format="channels_last"),
        Conv2D(32, (5, 5), data_format="channels_last"),
        Activation("relu"),
        ZeroPadding2D(padding=2, data_format="channels_last"),
        Conv2D(32, (5, 5), data_format="channels_last"),
        Activation("relu"),
        ZeroPadding2D(padding=2, data_format="channels_last"),
        Conv2D(32, (5, 5), data_format="channels_last"),
        Activation("relu"),
        Flatten(),
        Dense(512),
        Activation("relu"),
    ]


def create_model(encoder, go_board_rows, go_board_cols, num_classes):
    input_shape = (go_board_rows, go_board_cols, encoder.num_planes)
    network_layers = layers(input_shape)

    model = keras.Sequential()
    for layer in network_layers:
        model.add(layer)
    model.add(keras.layers.Dense(num_classes, activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])

    return model
