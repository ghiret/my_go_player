import keras
import numpy as np

from dlgo.data.sequence import DataSequence
from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo.networks import small

BOARD_SIZE = 19
NUM_CLASSES = BOARD_SIZE * BOARD_SIZE


def test_create_model_output_shape():
    encoder = OnePlaneEncoder((BOARD_SIZE, BOARD_SIZE))
    model = small.create_model(encoder, BOARD_SIZE, BOARD_SIZE, NUM_CLASSES)

    assert model.input_shape == (None, BOARD_SIZE, BOARD_SIZE, 1)
    assert model.output_shape == (None, NUM_CLASSES)


def test_model_trains_on_data_sequence(tmp_path):
    """Train one epoch from a DataSequence on the active Keras backend (KERAS_BACKEND)."""
    rng = np.random.default_rng(0)
    features = rng.integers(-1, 2, size=(8, 1, BOARD_SIZE, BOARD_SIZE)).astype("float32")
    labels = rng.integers(0, NUM_CLASSES, size=8)
    features_file, labels_file = tmp_path / "features.npy", tmp_path / "labels.npy"
    np.save(features_file, features)
    np.save(labels_file, labels)

    sequence = DataSequence(str(tmp_path), (str(features_file), str(labels_file)), batch_size=4, num_classes=NUM_CLASSES)
    encoder = OnePlaneEncoder((BOARD_SIZE, BOARD_SIZE))
    model = small.create_model(encoder, BOARD_SIZE, BOARD_SIZE, NUM_CLASSES)

    history = model.fit(sequence, epochs=1, verbose=0)
    probs = model.predict(features[:2].reshape(-1, BOARD_SIZE, BOARD_SIZE, 1), verbose=0)

    assert np.isfinite(history.history["loss"][0])
    assert probs.shape == (2, NUM_CLASSES)
    np.testing.assert_allclose(probs.sum(axis=1), 1.0, rtol=1e-4)
    assert keras.backend.backend() in {"jax", "tensorflow", "torch"}
