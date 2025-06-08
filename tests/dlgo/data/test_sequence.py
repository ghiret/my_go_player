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
def data_sequence(mock_data_directory, mock_samples):
    # Patch numpy.load as DataSequence loads data in __init__
    with patch("numpy.load") as mock_np_load:
        # Return simple empty arrays for features and labels for most tests
        mock_np_load.side_effect = [np.array([]), np.array([])]
        return DataSequence(mock_data_directory, mock_samples)


def test_init(data_sequence, mock_data_directory, mock_samples):
    assert data_sequence.data_directory == mock_data_directory
    assert data_sequence.features_file == mock_samples[0]
    assert data_sequence.labels_file == mock_samples[1]
    assert data_sequence.num_classes == 19 * 19


@patch("numpy.load")
def test_load_all_data(mock_np_load):
    mock_features_data = np.arange(6 * 361, dtype=np.float32).reshape(6, 1, 19, 19)
    mock_labels_data = np.array([0, 1, 2, 3, 4, 5])
    mock_np_load.side_effect = [mock_features_data, mock_labels_data]

    sequence = DataSequence("/mock/data", ("features.npy", "labels.npy"))

    assert sequence.num_samples == 6
    np.testing.assert_array_equal(sequence.features, mock_features_data)
    np.testing.assert_array_equal(sequence.labels, mock_labels_data)


def test_len(data_sequence):
    data_sequence.num_samples = 1000
    assert len(data_sequence) == 1000


def test_getitem(data_sequence):
    num_test_samples = 4
    # Each sample should have shape (1, 19, 19)
    mock_features = np.arange(num_test_samples * 1 * 19 * 19, dtype=np.float32).reshape(num_test_samples, 1, 19, 19)
    mock_raw_labels = np.array([0, 1, 2, 3])

    data_sequence.features = mock_features
    data_sequence.labels = mock_raw_labels
    data_sequence.num_samples = 4
    data_sequence.num_classes = 19 * 19

    # Now __getitem__ returns a single sample, not a batch
    sample_0 = data_sequence[0]
    assert isinstance(sample_0[0], torch.Tensor)
    assert isinstance(sample_0[1], torch.Tensor)
    # Features should be (1, 19, 19)
    assert sample_0[0].shape == (1, 19, 19)
    # Label should be a scalar
    assert sample_0[1].shape == ()
    # Check values
    np.testing.assert_array_equal(sample_0[0].numpy(), mock_features[0])
    np.testing.assert_array_equal(sample_0[1].numpy(), mock_raw_labels[0])

    sample_1 = data_sequence[1]
    assert sample_1[0].shape == (1, 19, 19)
    assert sample_1[1].shape == ()
    np.testing.assert_array_equal(sample_1[0].numpy(), mock_features[1])
    np.testing.assert_array_equal(sample_1[1].numpy(), mock_raw_labels[1])


def test_get_num_samples(data_sequence):
    data_sequence.num_samples = 1000
    assert len(data_sequence) == 1000
