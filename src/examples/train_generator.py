# This is a copy of https://github.com/maxpumperla/deep_learning_and_the_game_of_go/blob/master/code/examples/train_generator.py
"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code has been modified and adapted for use with Keras 3 and TensorFlow.
"""
import multiprocessing
import os
import traceback

import tensorflow as tf
from tensorflow import keras

from dlgo.data.processor import GoDataProcessor
from dlgo.data.sequence import DataSequence
from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo.networks import small


def main():
    go_board_rows, go_board_cols = 19, 19
    num_classes = go_board_rows * go_board_cols
    num_games = 100
    batch_size = 128

    encoder = OnePlaneEncoder((go_board_rows, go_board_cols))
    processor = GoDataProcessor(encoder=encoder.name())

    try:
        train_data = processor.load_go_data("train", num_games)
        test_data = processor.load_go_data("test", num_games)

        train_sequence = DataSequence(processor.data_dir, train_data, batch_size, num_classes)
        test_sequence = DataSequence(processor.data_dir, test_data, batch_size, num_classes)

        # Create the model using the new function
        model = small.create_model(encoder, go_board_rows, go_board_cols, num_classes)

        # Define the checkpoint callback
        checkpoint_callback = keras.callbacks.ModelCheckpoint(
            "../checkpoints/small_model_epoch_{epoch}.keras", save_best_only=True, monitor="val_accuracy"
        )

        # Train the model
        model.fit(train_sequence, epochs=5, validation_data=test_sequence, callbacks=[checkpoint_callback])

        # Evaluate the model
        evaluation_results = model.evaluate(test_sequence)

        print(f"Test loss: {evaluation_results[0]}")
        print(f"Test accuracy: {evaluation_results[1]}")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
    finally:
        # Clean up any resources if necessary
        pass


if __name__ == "__main__":

    # Set the start method for multiprocessing
    multiprocessing.set_start_method("spawn")

    # Set the number of OpenMP threads
    os.environ["OMP_NUM_THREADS"] = "1"

    # Run the main function
    main()
