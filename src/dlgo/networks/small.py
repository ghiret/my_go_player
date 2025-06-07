# Copied from https://github.com/maxpumperla/deep_learning_and_the_game_of_go/blob/master/code/dlgo/networks/small.py
from __future__ import absolute_import

import torch
import torch.nn as nn
import torch.nn.functional as F


class SmallGoCNN(nn.Module):
    def __init__(self, encoder, go_board_rows, go_board_cols, num_classes):
        super().__init__()
        in_channels = encoder.num_planes
        self.pad1 = nn.ZeroPad2d(3)  # (left, right, top, bottom)
        self.conv1 = nn.Conv2d(in_channels, 48, kernel_size=7, padding=0)
        self.pad2 = nn.ZeroPad2d(2)
        self.conv2 = nn.Conv2d(48, 32, kernel_size=5, padding=0)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=5, padding=0)
        self.conv4 = nn.Conv2d(32, 32, kernel_size=5, padding=0)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(self._get_flattened_size(go_board_rows, go_board_cols, in_channels), 512)
        self.fc2 = nn.Linear(512, num_classes)

    def _get_flattened_size(self, rows, cols, in_channels):
        # Compute the output size after all conv/pad layers for input shape (batch, in_channels, rows, cols)
        x = torch.zeros(1, in_channels, rows, cols)
        x = self.pad1(x)
        x = self.conv1(x)
        x = F.relu(x)
        x = self.pad2(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = self.pad2(x)
        x = self.conv3(x)
        x = F.relu(x)
        x = self.pad2(x)
        x = self.conv4(x)
        x = F.relu(x)
        x = self.flatten(x)
        return x.shape[1]

    def forward(self, x):
        x = self.pad1(x)
        x = self.conv1(x)
        x = F.relu(x)
        x = self.pad2(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = self.pad2(x)
        x = self.conv3(x)
        x = F.relu(x)
        x = self.pad2(x)
        x = self.conv4(x)
        x = F.relu(x)
        x = self.flatten(x)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.log_softmax(x, dim=1)  # Use log_softmax for classification
        return x


def create_model(encoder, go_board_rows, go_board_cols, num_classes):
    return SmallGoCNN(encoder, go_board_rows, go_board_cols, num_classes)
