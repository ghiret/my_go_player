# Copied from https://github.com/maxpumperla/deep_learning_and_the_game_of_go/blob/master/code/dlgo/data/parallel_processor.py
"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""
from __future__ import absolute_import, print_function

import glob
import gzip
import multiprocessing
import os
import os.path
import shutil
import sys
import tarfile

import numpy as np
from keras.utils import to_categorical

from dlgo.board import Board
from dlgo.data.index_processor import KGSIndex
from dlgo.data.sampling import Sampler
from dlgo.data.sequence import DataSequence
from dlgo.encoders.base import get_encoder_by_name
from dlgo.gamestate import GameState
from dlgo.gosgf.sgf import Sgf_game
from dlgo.gotypes import Player, Point
from dlgo.move import Move


def worker(jobinfo):
    try:
        clazz, encoder, zip_file, data_file_name, game_list = jobinfo
        clazz(encoder=encoder).process_zip(zip_file, data_file_name, game_list)
    except (KeyboardInterrupt, SystemExit):
        raise Exception(">>> Exiting child process.")


class GoDataProcessor:
    def __init__(self, encoder="simple", data_directory="data"):
        self.encoder_string = encoder
        self.encoder = get_encoder_by_name(encoder, 19)
        self.data_dir = data_directory

    def load_go_data(self, data_type="train", num_samples=1000):
        """
        Load Go data from the specified data_type and number of samples.

        Args:
            data_type (str): The type of data to load. Can be either 'train' or 'test'.
            num_samples (int): The number of games to load data from.

        Returns:
            features_and_labels (list): A list of features and labels for the loaded data.
        """
        index = KGSIndex(data_directory=self.data_dir)
        # We download all games from KGS to our local data directory. If data is available, it won't be downloaded again.
        index.download_files()

        sampler = Sampler(data_dir=self.data_dir)
        # The `Sampler` instance selects the specified number of games for a data type.
        data = sampler.draw_data(data_type, num_samples)
        zip_names = set()
        game_numbers_by_zip_name = {}
        for filename, game_number in data:
            print(f"filename= {filename} and game_number: {game_number}")
            # We collect all zip file names contained in the data in a list.
            zip_names.add(filename)
            if filename not in game_numbers_by_zip_name:
                game_numbers_by_zip_name[filename] = []
            # Then we group all SGF file game numbers by zip file name.
            game_numbers_by_zip_name[filename].append(game_number)
        for zip_name in zip_names:
            base_name = zip_name.replace(".tar.gz", "")
            data_file_name = base_name + data_type
            if not os.path.isfile(self.data_dir + "/" + data_file_name):
                # The zip files are then processed individually.
                self.process_zip(zip_name, data_file_name, game_numbers_by_zip_name[zip_name])
        # Features and labels from each zip are then aggregated and returned.
        features_and_labels = self.consolidate_games(data_type, data)
        return features_and_labels

    def unzip_data(self, zip_file_name):
        # Unpack the `gz` file into a `tar` file.
        this_gz = gzip.open(self.data_dir + "/" + zip_file_name)

        # Remove ".gz" at the end to get the name of the tar file.
        tar_file = zip_file_name[0:-3]
        this_tar = open(self.data_dir + "/" + tar_file, "wb")

        # Copy the contents of the unpacked file into the `tar` file.
        shutil.copyfileobj(this_gz, this_tar)
        this_tar.close()
        return tar_file

    def process_zip(self, zip_file_name, data_file_name, game_list):
        """
        Process a ZIP file containing SGF game files and extract data to update the game list.

        This method unzips the provided ZIP file, reads the SGF files within it, and processes
        each game to extract features and labels. The features and labels are encoded using
        the specified encoder.

        Args:
            zip_file_name (str): The name of the ZIP file to process.
            data_file_name (str): The base name for the output feature and label files.
            game_list (list): The list of game indices to process from the ZIP file.

        Raises:
            ValueError: If a file within the ZIP is not a valid SGF file.

        Returns:
            None
        """
        tar_file = self.unzip_data(zip_file_name)
        zip_file = tarfile.open(self.data_dir + "/" + tar_file)
        name_list = zip_file.getnames()
        # Determine the total number of moves in all games in this zip file.
        total_examples = self.num_total_examples(zip_file, game_list, name_list)
        # Infer the shape of features and labels from the encoder we use.
        shape = self.encoder.shape()
        feature_shape = np.insert(shape, 0, np.asarray([total_examples]))
        features = np.zeros(feature_shape)
        labels = np.zeros((total_examples,))

        counter = 0
        for index in game_list:
            name = name_list[index + 1]
            if not name.endswith(".sgf"):
                raise ValueError(name + " is not a valid sgf")
            sgf_content = zip_file.extractfile(name).read()

            # Read the SGF content as string, after extracting the zip file.
            sgf = Sgf_game.from_string(sgf_content)
            # Infer the initial game state by applying all handicap stones.
            game_state, first_move_done = self.get_handicap(sgf)

            # Iterate over all moves in the SGF file.
            for item in sgf.main_sequence_iter():
                color, move_tuple = item.get_move()
                point = None
                if color is not None:
                    # Read the coordinates of the stone to be played...
                    if move_tuple is not None:
                        row, col = move_tuple
                        point = Point(row + 1, col + 1)
                        move = Move.play(point)
                    else:
                        # ... or pass, if there is none.
                        move = Move.pass_turn()
                    if first_move_done and point is not None:
                        # We encode the current game state as features...
                        features[counter] = self.encoder.encode(game_state)
                        # ... and the next move as label for the features.
                        labels[counter] = self.encoder.encode_point(point)
                        counter += 1
                    # Afterwards the move is applied to the board and we proceed with the next one.
                    game_state = game_state.apply_move(move)
                    first_move_done = True

        feature_file_base = self.data_dir + "/" + data_file_name + "_features_%d"
        label_file_base = self.data_dir + "/" + data_file_name + "_labels_%d"

        chunk = 0  # Due to files with large content, split up after chunksize
        chunksize = 1024
        # We process features and labels in chunks of size 1024.
        while features.shape[0] >= chunksize:
            feature_file = feature_file_base % chunk
            label_file = label_file_base % chunk
            chunk += 1
            current_features, features = features[:chunksize], features[chunksize:]
            # The current chunk is cut off from features and labels...
            current_labels, labels = labels[:chunksize], labels[chunksize:]
            np.save(feature_file, current_features)
            # ...  and then stored in a separate file.
            np.save(label_file, current_labels)

    def consolidate_games(self, data_type, samples):
        files_needed = set(file_name for file_name, index in samples)
        file_names = []
        for zip_file_name in files_needed:
            file_name = zip_file_name.replace(".tar.gz", "") + data_type
            file_names.append(file_name)

        feature_list = []
        label_list = []
        for file_name in file_names:
            file_prefix = file_name.replace(".tar.gz", "")
            base = self.data_dir + "/" + file_prefix + "_features_*.npy"
            for feature_file in glob.glob(base):
                label_file = feature_file.replace("features", "labels")
                x = np.load(feature_file)
                y = np.load(label_file)
                x = x.astype("float32")
                y = to_categorical(y.astype(int), 19 * 19)
                feature_list.append(x)
                label_list.append(y)
        features = np.concatenate(feature_list, axis=0)
        labels = np.concatenate(label_list, axis=0)

        features_filename = f"{self.data_dir}/features_{data_type}.npy"
        labels_filename = f"{self.data_dir}/labels_{data_type}.npy"

        np.save(features_filename, features)
        np.save(labels_filename, labels)

        return features_filename, labels_filename

    @staticmethod
    def get_handicap(sgf):
        go_board = Board(19, 19)
        first_move_done = False
        move = None
        game_state = GameState.new_game(19)
        if sgf.get_handicap() is not None and sgf.get_handicap() != 0:
            for setup in sgf.get_root().get_setup_stones():
                for move in setup:
                    row, col = move
                    go_board.place_stone(Player.black, Point(row + 1, col + 1))
            first_move_done = True
            game_state = GameState(go_board, Player.white, None, move)
        return game_state, first_move_done

    def map_to_workers(self, data_type, samples):
        zip_names = set()
        indices_by_zip_name = {}
        for filename, index in samples:
            zip_names.add(filename)
            if filename not in indices_by_zip_name:
                indices_by_zip_name[filename] = []
            indices_by_zip_name[filename].append(index)

        zips_to_process = []
        for zip_name in zip_names:
            base_name = zip_name.replace(".tar.gz", "")
            data_file_name = base_name + data_type
            if not os.path.isfile(self.data_dir + "/" + data_file_name):
                zips_to_process.append((self.__class__, self.encoder_string, zip_name, data_file_name, indices_by_zip_name[zip_name]))

        cores = multiprocessing.cpu_count()  # Determine number of CPU cores and split work load among them
        pool = multiprocessing.Pool(processes=cores)
        p = pool.map_async(worker, zips_to_process)
        try:
            _ = p.get()
        except KeyboardInterrupt:  # Caught keyboard interrupt, terminating workers
            pool.terminate()
            pool.join()
            sys.exit(-1)

    def num_total_examples(self, zip_file, game_list, name_list):
        total_examples = 0
        for index in game_list:
            name = name_list[index + 1]
            if name.endswith(".sgf"):
                sgf_content = zip_file.extractfile(name).read()
                sgf = Sgf_game.from_string(sgf_content)
                game_state, first_move_done = self.get_handicap(sgf)

                num_moves = 0
                for item in sgf.main_sequence_iter():
                    color, move = item.get_move()
                    if color is not None:
                        if first_move_done:
                            num_moves += 1
                        first_move_done = True
                total_examples = total_examples + num_moves
            else:
                raise ValueError(name + " is not a valid sgf")
        return total_examples
