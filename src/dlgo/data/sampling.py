# Copied from https://github.com/maxpumperla/deep_learning_and_the_game_of_go/blob/master/code/dlgo/data/sampling.py
"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import absolute_import, print_function

import os
import random

from six.moves import range

from dlgo.data.index_processor import KGSIndex


class Sampler:
    """Sample training and test data from zipped sgf files such that test data is kept stable."""

    def __init__(self, data_dir="data", num_test_games=100, cap_year=2015, seed=1337):
        self.data_dir = data_dir
        self.num_test_games = num_test_games
        self.test_games = []
        self.train_games = []
        self.test_folder = "test_samples.py"
        self.cap_year = cap_year

        random.seed(seed)
        self.compute_test_samples()

    def draw_data(self, data_type, num_samples):
        if data_type == "test":
            return self.test_games
        elif data_type == "train" and num_samples is not None:
            return self.draw_training_samples(num_samples)
        elif data_type == "train" and num_samples is None:
            return self.draw_all_training()
        else:
            raise ValueError(data_type + " is not a valid data type, choose from 'train' or 'test'")

    def draw_samples(self, num_sample_games):
        """Draw num_sample_games many training games from index."""
        available_games = []
        index = KGSIndex(data_directory=self.data_dir)

        for fileinfo in index.file_info:
            filename = fileinfo["filename"]
            year = int(filename.split("-")[1].split("_")[0])
            if year > self.cap_year:
                continue
            num_games = fileinfo["num_games"]
            for i in range(num_games):
                available_games.append((filename, i))
        print(">>> Total number of games used: " + str(len(available_games)))

        sample_set = set()
        while len(sample_set) < num_sample_games:
            sample = random.choice(available_games)
            if sample not in sample_set:
                sample_set.add(sample)
        print("Drawn " + str(num_sample_games) + " samples:")
        return list(sample_set)

    def draw_training_games(self):
        """Get list of all non-test games, that are no later than dec 2014
        Ignore games after cap_year to keep training data stable
        """
        index = KGSIndex(data_directory=self.data_dir)
        for file_info in index.file_info:
            filename = file_info["filename"]
            year = int(filename.split("-")[1].split("_")[0])
            if year > self.cap_year:
                continue
            num_games = file_info["num_games"]
            for i in range(num_games):
                sample = (filename, i)
                if sample not in self.test_games:
                    self.train_games.append(sample)
        print("total num training games: " + str(len(self.train_games)))

    def compute_test_samples(self):
        """If not already existing, create local file to store fixed set of test samples"""
        if not os.path.isfile(self.test_folder):
            test_games = self.draw_samples(self.num_test_games)
            test_sample_file = open(self.test_folder, "w")
            for sample in test_games:
                test_sample_file.write(str(sample) + "\n")
            test_sample_file.close()

        test_sample_file = open(self.test_folder, "r")
        sample_contents = test_sample_file.read()
        test_sample_file.close()
        for line in sample_contents.split("\n"):
            if line != "":
                (filename, index) = eval(line)
                self.test_games.append((filename, index))

    def draw_training_samples(self, num_sample_games: int):
        """
        Draw a specified number of training game samples, ensuring no overlap with test games.

        This method selects random game samples from available game files up to a certain year.
        It ensures that the selected samples are not part of the predefined test set.

        Args:
            num_sample_games (int): The number of game samples to draw.

        Returns:
            List[Tuple[str, int]]: A list of tuples, each containing a filename and game number,
            representing the selected game samples.

        Raises:
            ValueError: If num_sample_games is greater than the number of available games.

        Note:
            - The method uses self.data_dir to locate game data.
            - It respects self.cap_year as the upper limit for game file years.
            - It assumes self.test_games is a pre-existing set of games to be excluded.
        """

        # Initialize an empty list to store all available games
        available_games = []

        # Create an index object to access game data
        index = KGSIndex(data_directory=self.data_dir)

        # Iterate through each file in the index
        for fileinfo in index.file_info:
            filename = fileinfo["filename"]

            # Extract the year from the filename
            year = int(filename.split("-")[1].split("_")[0])

            # Skip files from years after the cap year
            if year > self.cap_year:
                continue

            # Get the number of games in this file
            num_games = fileinfo["num_games"]

            # Add each game from this file to the available_games list
            for game_number in range(num_games):
                available_games.append((filename, game_number))
                print((filename, game_number))  # Print each game added

        # Print the total number of available games
        print(f"Total number of games: {len(available_games)}")

        # Check if we have enough games to sample from
        if num_sample_games > len(available_games):
            raise ValueError("Not enough games to sample from")

        # Initialize an empty set to store the selected samples
        sample_set = set()  # type: ignore

        # Keep selecting random samples until we have the desired number
        while len(sample_set) < num_sample_games:
            # Randomly choose a game from available_games
            sample = random.choice(available_games)

            # Only add the sample if it's not in the test set
            if sample not in self.test_games:
                sample_set.add(sample)

        # Print the number of samples drawn
        print(f"Drawn {num_sample_games} samples")

        # Return the sample set as a list
        return list(sample_set)

    def draw_all_training(self):
        """Draw all available training games."""
        available_games = []
        index = KGSIndex(data_directory=self.data_dir)

        for fileinfo in index.file_info:
            filename = fileinfo["filename"]
            year = int(filename.split("-")[1].split("_")[0])
            if year > self.cap_year:
                continue
            if "num_games" in fileinfo.keys():
                num_games = fileinfo["num_games"]
            else:
                continue
            for i in range(num_games):
                available_games.append((filename, i))
        print("total num games: " + str(len(available_games)))

        sample_set = set()
        for sample in available_games:
            if sample not in self.test_games:
                sample_set.add(sample)
        print("Drawn all samples, ie " + str(len(sample_set)) + " samples:")
        return list(sample_set)
