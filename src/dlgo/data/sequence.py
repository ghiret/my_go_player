# Copied from https://github.com/maxpumperla/deep_learning_and_the_game_of_go/blob/master/code/dlgo/data/generator.py
"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
This has been adapted to keras v3 using Anthropic's Claude model.
"""
import glob

import numpy as np
from tensorflow.keras.utils import Sequence, to_categorical


class DataSequence(Sequence):
    def __init__(self, data_directory, samples, batch_size=128, num_classes=19 * 19):
        super().__init__()
        self.data_directory = data_directory
        self.features_file, self.labels_file = samples
        self.batch_size = batch_size
        self.num_classes = num_classes

        # Load all data into memory
        self.features = np.load(self.features_file)
        self.labels = np.load(self.labels_file)

        self.num_samples = len(self.features)

    def __len__(self):
        return int(np.ceil(self.num_samples / float(self.batch_size)))

    def __getitem__(self, idx):
        start = idx * self.batch_size
        end = min((idx + 1) * self.batch_size, self.num_samples)
        batch_features = self.features[start:end]
        batch_labels = self.labels[start:end]

        # Print shapes before reshaping and encoding
        # print(f"Original batch_features shape: {batch_features.shape}")
        # print(f"Original batch_labels shape: {batch_labels.shape}")

        # Ensure features are in the correct shape (batch_size, 19, 19, 1)
        batch_features = batch_features.reshape(-1, 19, 19, 1)

        # Print shapes after reshaping
        # print(f"Reshaped batch_features shape: {batch_features.shape}")

        # Ensure labels are integers before one-hot encoding
        # print(batch_labels)
        # Print shapes before one-hot encoding
        # print(f"batch_labels shape: {batch_labels.shape}")
        if batch_labels.ndim > 1 and batch_labels.shape[1] == self.num_classes:
            batch_labels = np.argmax(batch_labels, axis=1)

        # Convert labels to one-hot encoding with the correct shape (batch_size, 361)
        batch_labels = to_categorical(batch_labels, self.num_classes)

        # Print shapes after one-hot encoding
        # print(f"One-hot encoded batch_labels shape: {batch_labels.shape}")

        return batch_features, batch_labels

    def get_num_samples(self):
        return self.num_samples
