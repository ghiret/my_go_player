# Copied from https://github.com/maxpumperla/deep_learning_and_the_game_of_go/blob/master/code/dlgo/data/generator.py
"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
This has been adapted to keras v3 using Anthropic's Claude model.
"""
import numpy as np
import torch
from torch.utils.data import Dataset


class DataSequence(Dataset):
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

        batch_features = torch.from_numpy(batch_features).float()

        # If labels are already one-hot, convert to class indices
        if batch_labels.ndim > 1 and batch_labels.shape[1] == self.num_classes:
            batch_labels = np.argmax(batch_labels, axis=1)

        # Convert labels to torch tensor (class indices)
        batch_labels = torch.from_numpy(batch_labels).long()

        return batch_features, batch_labels

    def get_num_samples(self):
        return self.num_samples
