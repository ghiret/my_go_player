from unittest.mock import mock_open, patch

import numpy as np
import pytest
from keras.utils import to_categorical

from dlgo.data.generator import DataGenerator  # Updated import path


@pytest.fixture
def mock_data_directory():
    return "/mock/data/directory"


@pytest.fixture
def mock_samples():
    return [("file1.tar.gz", 0), ("file2.tar.gz", 1)]


@pytest.fixture
def data_generator(mock_data_directory, mock_samples):
    return DataGenerator(mock_data_directory, mock_samples)


def test_init(data_generator, mock_data_directory, mock_samples):
    assert data_generator.data_directory == mock_data_directory
    assert data_generator.samples == mock_samples
    assert data_generator.files == {"file1.tar.gz", "file2.tar.gz"}
    assert data_generator.num_samples is None


@patch("glob.glob")
@patch("numpy.load")
def test_generate(mock_np_load, mock_glob, data_generator):
    mock_glob.return_value = ["/mock/data/directory/file1train_features_1.npy"]
    mock_np_load.side_effect = [np.array([[1, 2], [3, 4], [5, 6]]), np.array([0, 1, 2])]  # Features  # Labels

    generator = data_generator.generate(batch_size=2, num_classes=3)
    batch = next(generator)

    assert len(batch) == 2
    assert batch[0].shape == (2, 2)
    assert batch[1].shape == (2, 3)
    np.testing.assert_array_equal(batch[0], np.array([[1, 2], [3, 4]], dtype="float32"))
    np.testing.assert_array_equal(batch[1], to_categorical(np.array([0, 1]), num_classes=3))


def test_get_num_samples(data_generator):
    with patch.object(DataGenerator, "_generate") as mock_generate:
        mock_generate.return_value = iter(
            [(np.zeros((10, 19, 19, 17)), np.zeros((10, 361))), (np.zeros((5, 19, 19, 17)), np.zeros((5, 361)))]
        )

        num_samples = data_generator.get_num_samples()
        assert num_samples == 15
        assert data_generator.num_samples == 15

        # Test caching
        data_generator.get_num_samples()
        mock_generate.assert_called_once()
