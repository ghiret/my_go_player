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
    # DataSequence expects a tuple of (features_filepath, labels_filepath)
    return ("mock_features.npy", "mock_labels.npy")


@pytest.fixture
def data_generator(mock_data_directory, mock_samples):
    # Patch numpy.load as DataSequence loads data in __init__
    with patch("numpy.load") as mock_np_load:
        # Return simple empty arrays for features and labels for most tests
        # Adjust if specific tests using this fixture need more complex mock data
        mock_np_load.side_effect = [np.array([]), np.array([])]
        return DataSequence(mock_data_directory, mock_samples)


def test_init(data_generator, mock_data_directory, mock_samples):
    assert data_generator.data_directory == mock_data_directory
    # Check for the unpacked file paths
    assert data_generator.features_file == mock_samples[0]
    assert data_generator.labels_file == mock_samples[1]
    # DataSequence does not have a 'files' or 'samples' attribute after __init__
    assert data_generator.batch_size == 128
    assert data_generator.num_classes == 19 * 19


@patch("numpy.load")
def test_load_all_data(mock_np_load):
    # glob.glob is not used by the current DataSequence implementation
    mock_features_data = np.array([[1, 2], [3, 4], [5, 6]])
    mock_labels_data = np.array([0, 1, 2])
    mock_np_load.side_effect = [mock_features_data, mock_labels_data]

    # Provide a tuple of (features_filepath, labels_filepath) for samples
    generator = DataSequence("/mock/data", ("features.npy", "labels.npy"))

    assert generator.num_samples == 3
    # DataSequence stores data in .features and .labels
    np.testing.assert_array_equal(generator.features, mock_features_data)
    np.testing.assert_array_equal(generator.labels, mock_labels_data)


def test_len(data_generator):
    data_generator.num_samples = 1000
    data_generator.batch_size = 128
    assert len(data_generator) == 8  # ceil(1000/128) = 8


def test_getitem(data_generator):
    num_test_samples = 4
    feature_length = 19 * 19 * 1  # Each sample should have 19*19*1 features
    # Create mock features with the correct flattened shape per sample
    mock_features = np.arange(num_test_samples * feature_length, dtype=np.float32).reshape(num_test_samples, feature_length)
    mock_raw_labels = np.array([0, 1, 2, 3])  # Raw labels before one-hot encoding

    # Set the features and labels directly on the fixture instance
    data_generator.features = mock_features
    data_generator.labels = mock_raw_labels
    data_generator.num_samples = 4
    data_generator.batch_size = 2
    data_generator.num_classes = 19 * 19  # Ensure num_classes is set for to_categorical

    batch_0 = data_generator[0]
    assert len(batch_0) == 2
    # Features are reshaped in __getitem__
    expected_features_batch_0 = mock_features[0:2].reshape(-1, 19, 19, 1)
    np.testing.assert_array_equal(batch_0[0], expected_features_batch_0)
    np.testing.assert_array_equal(batch_0[1], to_categorical(mock_raw_labels[0:2], num_classes=19 * 19))

    batch_1 = data_generator[1]
    assert len(batch_1) == 2
    expected_features_batch_1 = mock_features[2:4].reshape(-1, 19, 19, 1)
    np.testing.assert_array_equal(batch_1[0], expected_features_batch_1)
    np.testing.assert_array_equal(batch_1[1], to_categorical(mock_raw_labels[2:4], num_classes=19 * 19))


def test_get_num_samples(data_generator):
    data_generator.num_samples = 1000
    assert data_generator.get_num_samples() == 1000
