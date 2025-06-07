from unittest.mock import patch

import numpy as np
import pytest
import torch

from dlgo.data.sequence import DataSequence


@pytest.fixture
def mock_data_directory():
    return "/mock/data/directory"


@pytest.fixture
def mock_samples():
    # DataSequence expects a tuple of (features_filepath, labels_filepath)
    return ("mock_features.npy", "mock_labels.npy")


@pytest.fixture
def data_generator(mock_data_directory, mock_samples):
    # Patch numpy.load as DataSequence loads data in __init__
    with patch("numpy.load") as mock_np_load:
        # Return simple empty arrays for features and labels for most tests
        mock_np_load.side_effect = [np.array([]), np.array([])]
        return DataSequence(mock_data_directory, mock_samples)


def test_init(data_generator, mock_data_directory, mock_samples):
    assert data_generator.data_directory == mock_data_directory
    assert data_generator.features_file == mock_samples[0]
    assert data_generator.labels_file == mock_samples[1]
    assert data_generator.batch_size == 128
    assert data_generator.num_classes == 19 * 19


@patch("numpy.load")
def test_load_all_data(mock_np_load):
    mock_features_data = np.arange(6 * 361, dtype=np.float32).reshape(6, 1, 19, 19)
    mock_labels_data = np.array([0, 1, 2, 3, 4, 5])
    mock_np_load.side_effect = [mock_features_data, mock_labels_data]

    generator = DataSequence("/mock/data", ("features.npy", "labels.npy"))

    assert generator.num_samples == 6
    np.testing.assert_array_equal(generator.features, mock_features_data)
    np.testing.assert_array_equal(generator.labels, mock_labels_data)


def test_len(data_generator):
    data_generator.num_samples = 1000
    data_generator.batch_size = 128
    assert len(data_generator) == 8  # ceil(1000/128) = 8


def test_getitem(data_generator):
    num_test_samples = 4
    # Each sample should have shape (1, 19, 19)
    mock_features = np.arange(num_test_samples * 1 * 19 * 19, dtype=np.float32).reshape(num_test_samples, 1, 19, 19)
    mock_raw_labels = np.array([0, 1, 2, 3])

    data_generator.features = mock_features
    data_generator.labels = mock_raw_labels
    data_generator.num_samples = 4
    data_generator.batch_size = 2
    data_generator.num_classes = 19 * 19

    batch_0 = data_generator[0]
    assert isinstance(batch_0[0], torch.Tensor)
    assert isinstance(batch_0[1], torch.Tensor)
    # Features should be (batch, 1, 19, 19)
    assert batch_0[0].shape == (2, 1, 19, 19)
    # Labels should be (batch,)
    assert batch_0[1].shape == (2,)
    # Check values
    np.testing.assert_array_equal(batch_0[0].numpy(), mock_features[0:2])
    np.testing.assert_array_equal(batch_0[1].numpy(), mock_raw_labels[0:2])

    batch_1 = data_generator[1]
    assert batch_1[0].shape == (2, 1, 19, 19)
    assert batch_1[1].shape == (2,)
    np.testing.assert_array_equal(batch_1[0].numpy(), mock_features[2:4])
    np.testing.assert_array_equal(batch_1[1].numpy(), mock_raw_labels[2:4])


def test_get_num_samples(data_generator):
    data_generator.num_samples = 1000
    assert data_generator.get_num_samples() == 1000
