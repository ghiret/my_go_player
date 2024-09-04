# This is a copy of https://github.com/maxpumperla/deep_learning_and_the_game_of_go/blob/master/code/examples/chapter_6_cnn/mcts_go_cnn_simple.py
"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""
from __future__ import print_function

# tag::mcts_go_cnn_simple_preprocessing[]
import numpy as np
import tensorflow as tf
from check_for_gpu import check_gpu_availability
from keras.layers import Conv2D, Dense, Flatten  # <1>
from keras.models import Sequential

check_gpu_availability()
np.random.seed(123)
X = np.load("src/dlgo/generated_games/features-40k.npy")
Y = np.load("src/dlgo/generated_games/labels-40k.npy")

samples = X.shape[0]
size = 9
input_shape = (size, size, 1)  # <2>

X = X.reshape(samples, size, size, 1)  # <3>

train_samples = int(0.9 * samples)
X_train, X_test = X[:train_samples], X[train_samples:]
Y_train, Y_test = Y[:train_samples], Y[train_samples:]

# <1> We import two new layers, a 2D convolutional layer and one that flattens its input to vectors.
# <2> The input data shape is 3-dimensional, we use one plane of a 9x9 board representation.
# <3> We then reshape our input data accordingly.
# end::mcts_go_cnn_simple_preprocessing[]

# tag::mcts_go_cnn_simple_model[]
model = Sequential()
model.add(Conv2D(filters=48, kernel_size=(3, 3), activation="sigmoid", padding="same", input_shape=input_shape))  # <1>  # <2>  # <3>

model.add(Conv2D(48, (3, 3), padding="same", activation="sigmoid"))  # <4>

model.add(Flatten())  # <5>

model.add(Dense(512, activation="sigmoid"))
model.add(Dense(size * size, activation="sigmoid"))  # <6>
model.summary()

# <1> The first layer in our network is a Conv2D layer with 48 output filters.
# <2> For this layer we choose a 3 by 3 convolutional kernel.
# <3> Normally the output of a convolution is smaller than the input. By adding `padding='same'`, we ask Keras to pad our matrix with zeros around the edges, so the output has the same dimension as the input.
# <4> The second layer is another convolution. We leave out the "filters" and "kernel_size" arguments for brevity.
# <5> We then flatten the 3D output of the previous convolutional layer...
# <6> ... and follow up with two more dense layers, as we did in the MLP example.
# end::mcts_go_cnn_simple_model[]

# tag::mcts_go_cnn_simple_eval[]
model.compile(loss="mean_squared_error", optimizer="sgd", metrics=["accuracy"])

model.fit(X_train, Y_train, batch_size=64, epochs=15, verbose=1, validation_data=(X_test, Y_test))

score = model.evaluate(X_test, Y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])
# end::mcts_go_cnn_eval[]
