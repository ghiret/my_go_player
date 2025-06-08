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
    def __init__(self, data_directory, samples, num_classes=19 * 19):
        super().__init__()
        self.data_directory = data_directory
        self.features_file, self.labels_file = samples
        self.num_classes = num_classes

        self.features = np.load(self.features_file)
        self.labels = np.load(self.labels_file)
        self.num_samples = len(self.features)

    def __len__(self):
        # __len__ should return the TOTAL number of samples in the dataset
        return self.num_samples

    def __getitem__(self, idx):
        # __getitem__ should return a SINGLE sample for the given index
        feature = self.features[idx]
        label = self.labels[idx]

        # Reshape the single feature to the format the model expects (C, H, W)
        # The original .npy file might have a shape like (1, 19, 19), so this is robust.
        # Assuming features are saved correctly with channel dimension.
        feature_tensor = torch.from_numpy(feature).float()
        assert feature_tensor.shape == (1, 19, 19), f"Unexpected feature shape: {feature_tensor.shape}"

        # If the label is one-hot encoded, convert it to a class index
        if label.ndim > 0 and label.size == self.num_classes:
            label_index = np.argmax(label)
        else:
            label_index = int(label)

        label_tensor = torch.tensor(label_index, dtype=torch.long)

        return feature_tensor, label_tensor
