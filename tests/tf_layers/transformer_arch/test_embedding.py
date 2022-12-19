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


def test_the_positional_encoding_layer_takes_as_input_vectors_in_this_shape(seq, pos_layer):
    # the input of positional encoding layer
    # should be in shape (batch size, seq length, embedding dim)
    # ie like the output of `Encoding` layer

    embedding_layer = tf.keras.layers.Embedding(input_dim=MAX_TOKENS, output_dim=EMBEDDING_DIM)
    proper_input = embedding_layer(seq)
    # process without error
    pos_layer(proper_input)
    pos_layer(np.zeros_like(proper_input.numpy()))