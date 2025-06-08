# Copied from https://github.com/maxpumperla/deep_learning_and_the_game_of_go/blob/master/code/dlgo/networks/small.py
from __future__ import absolute_import

import torch.nn as nn
import torch.nn.functional as F


class SmallGoCNN(nn.Module):
    def __init__(self, encoder, go_board_rows, go_board_cols, num_classes):
        super().__init__()
        in_channels = encoder.num_planes

        # Use built-in padding in Conv2d instead of ZeroPad2d
        self.conv1 = nn.Conv2d(in_channels, 48, kernel_size=7, padding=3)
        self.conv2 = nn.Conv2d(48, 32, kernel_size=5, padding=2)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=5, padding=2)
        self.conv4 = nn.Conv2d(32, 32, kernel_size=5, padding=2)

        # Output size after convs is [batch_size, 32, 19, 19] → flatten to 32*19*19
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(32 * go_board_rows * go_board_cols, 512)
        self.fc2 = nn.Linear(512, num_classes)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = self.flatten(x)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def create_model(encoder, go_board_rows, go_board_cols, num_classes):
    return SmallGoCNN(encoder, go_board_rows, go_board_cols, num_classes)
