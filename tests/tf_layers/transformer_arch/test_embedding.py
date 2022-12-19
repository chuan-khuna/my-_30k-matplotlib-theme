import numpy as np
import os
from unittest.mock import patch, MagicMock, Mock
import pytest
import warnings

warnings.filterwarnings('ignore')

import tensorflow as tf

from utils.tf_layers.transformer_arch.embedding import FixedPositionalEncoding

TEST_PATH = os.path.dirname(__file__)

SEQ_LENGTH = 128
EMBEDDING_DIM = 32
BATCH_SIZE = 4
MAX_TOKENS = 1024
DATA_SHAPE = (BATCH_SIZE, SEQ_LENGTH, EMBEDDING_DIM)


def get_tensor_shape(tensor):
    return tuple(tensor.shape)


@pytest.fixture
def seq():
    sequence = np.random.randint(low=0, high=MAX_TOKENS, size=(BATCH_SIZE, SEQ_LENGTH))
    return sequence


@pytest.fixture
def pos_layer():
    pos_layer = FixedPositionalEncoding(SEQ_LENGTH, EMBEDDING_DIM)
    return pos_layer


def test_architecture(seq, pos_layer):

    # ensure sequence data is batched
    assert seq.shape == (BATCH_SIZE, SEQ_LENGTH)

    # pass it through embedding layer
    embedding_layer = tf.keras.layers.Embedding(input_dim=MAX_TOKENS, output_dim=EMBEDDING_DIM)
    em_seq = embedding_layer(seq)
    assert get_tensor_shape(em_seq) == DATA_SHAPE

    # add positional encoding via using my layer
    pos_em_seq = pos_layer(em_seq)
    # data shape should not be changed
    assert get_tensor_shape(pos_em_seq) == DATA_SHAPE
    # data should be added with positional encoding
    assert (pos_em_seq.numpy() != em_seq.numpy()).all()