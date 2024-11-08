from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from tensorflow.keras.utils import to_categorical

from dlgo.data.sequence import DataSequence  # Updated import path


@pytest.fixture
def mock_data_directory():
    return "/mock/data/directory"


@pytest.fixture
def mock_samples():
    return [("file1.tar.gz", 0), ("file2.tar.gz", 1)]


@pytest.fixture
def data_generator(mock_data_directory, mock_samples):
    with patch.object(DataSequence, "_load_all_data", return_value=(np.array([]), np.array([]))):
        return DataSequence(mock_data_directory, mock_samples)


def test_init(data_generator, mock_data_directory, mock_samples):
    assert data_generator.data_directory == mock_data_directory
    assert data_generator.samples == mock_samples
    assert data_generator.files == {"file1.tar.gz", "file2.tar.gz"}
    assert data_generator.batch_size == 128
    assert data_generator.num_classes == 19 * 19


@patch("glob.glob")
@patch("numpy.load")
def test_load_all_data(mock_np_load, mock_glob):
    mock_glob.return_value = ["/mock/data/directory/file1train_features_1.npy"]
    mock_np_load.side_effect = [np.array([[1, 2], [3, 4], [5, 6]]), np.array([0, 1, 2])]  # Features  # Labels

    generator = DataSequence("/mock/data", [("file1.tar.gz", 0)])

    assert generator.num_samples == 3
    np.testing.assert_array_equal(generator.data[0], np.array([[1, 2], [3, 4], [5, 6]], dtype="float32"))
    np.testing.assert_array_equal(generator.data[1], to_categorical(np.array([0, 1, 2]), num_classes=19 * 19))


def test_len(data_generator):
    data_generator.num_samples = 1000
    data_generator.batch_size = 128
    assert len(data_generator) == 8  # ceil(1000/128) = 8


def test_getitem(data_generator):
    mock_data = (np.array([[1, 2], [3, 4], [5, 6], [7, 8]]), to_categorical(np.array([0, 1, 2, 3]), num_classes=19 * 19))
    data_generator.data = mock_data
    data_generator.num_samples = 4
    data_generator.batch_size = 2

    batch_0 = data_generator[0]
    assert len(batch_0) == 2
    np.testing.assert_array_equal(batch_0[0], np.array([[1, 2], [3, 4]]))
    np.testing.assert_array_equal(batch_0[1], to_categorical(np.array([0, 1]), num_classes=19 * 19))

    batch_1 = data_generator[1]
    assert len(batch_1) == 2
    np.testing.assert_array_equal(batch_1[0], np.array([[5, 6], [7, 8]]))
    np.testing.assert_array_equal(batch_1[1], to_categorical(np.array([2, 3]), num_classes=19 * 19))


def test_get_num_samples(data_generator):
    data_generator.num_samples = 1000
    assert data_generator.get_num_samples() == 1000
