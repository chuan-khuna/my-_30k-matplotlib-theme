import numpy as np
import os
from unittest.mock import patch, MagicMock, Mock
import pytest
import warnings

warnings.filterwarnings('ignore')

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Embedding

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
def zero_seq():
    zero_sequence = np.zeros(shape=(BATCH_SIZE, SEQ_LENGTH))
    return zero_sequence


def test_embedding_layer_output_shape(seq):
    # embedding layer take a batched tensor (b, seq)
    # it should return an output in shoe (b, seq, em)
    em_layer = Embedding(input_dim=MAX_TOKENS, output_dim=EMBEDDING_DIM, mask_zero=True)
    em_seq = em_layer(seq)

    # it should have keras mask
    # True for non-Zero value; False = zero
    em_seq._keras_mask

    assert get_tensor_shape(em_seq) == DATA_SHAPE


def test_embedding_layer_masking(zero_seq):
    em_layer = Embedding(input_dim=MAX_TOKENS, output_dim=EMBEDDING_DIM, mask_zero=True)
    em_seq = em_layer(zero_seq)

    # Since all of values in the sequence are zero
    # the masking values should be all False
    assert not em_seq._keras_mask.numpy().all()


def test_embedding_with_positional_encoding_output_shape(seq):
    em_layer = Embedding(input_dim=MAX_TOKENS, output_dim=EMBEDDING_DIM, mask_zero=True)
    pos_layer = FixedPositionalEncoding(SEQ_LENGTH, EMBEDDING_DIM)

    em_seq = em_layer(seq)
    pos_em_seq = pos_layer(em_seq)

    assert get_tensor_shape(pos_em_seq) == DATA_SHAPE
    assert get_tensor_shape(pos_em_seq) == get_tensor_shape(em_seq)


def test_positional_encoding_value(zero_seq):
    em_layer = Embedding(input_dim=MAX_TOKENS, output_dim=EMBEDDING_DIM, mask_zero=True)
    pos_layer = FixedPositionalEncoding(SEQ_LENGTH, EMBEDDING_DIM)

    em_seq = em_layer(zero_seq)
    pos_em_seq = pos_layer(em_seq)

    assert (em_seq.numpy() != pos_em_seq.numpy()).any()
