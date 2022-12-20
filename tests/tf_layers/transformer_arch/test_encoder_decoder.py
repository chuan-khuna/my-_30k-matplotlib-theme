import numpy as np
import os
from unittest.mock import patch, MagicMock, Mock
import pytest
import warnings

warnings.filterwarnings('ignore')

import tensorflow as tf
from tensorflow import keras

from utils.tf_layers.transformer_arch.embedding import PositionalEmbedding
from utils.tf_layers.transformer_arch.transformer import TransformerEncoderBlock, TransformerDecoderBlock
from utils.tf_layers.transformer_arch.model import Encoder, Decoder

TEST_PATH = os.path.dirname(__file__)

SEQ_LENGTH = 128
EMBEDDING_DIM = 32
BATCH_SIZE = 4
MAX_TOKENS = 1024
DATA_SHAPE = (BATCH_SIZE, SEQ_LENGTH, EMBEDDING_DIM)
NUM_HEADS = 8


def get_tensor_shape(tensor):
    return tuple(tensor.shape)


@pytest.fixture
def seq():
    sequence = np.random.randint(low=0, high=MAX_TOKENS, size=(BATCH_SIZE, SEQ_LENGTH))
    return sequence


def test_encoder(seq):
    enc = Encoder(num_layers=4,
                  num_heads=NUM_HEADS,
                  vocab_size=MAX_TOKENS,
                  embedding_dim=EMBEDDING_DIM)
    encoded_seq = enc(seq)

    assert get_tensor_shape(encoded_seq) == DATA_SHAPE


def test_encoder_decoder(seq):

    enc = Encoder(num_layers=4,
                  num_heads=NUM_HEADS,
                  vocab_size=MAX_TOKENS,
                  embedding_dim=EMBEDDING_DIM)
    context = enc(seq)

    dec = Decoder(num_layers=4,
                  num_heads=NUM_HEADS,
                  vocab_size=MAX_TOKENS,
                  embedding_dim=EMBEDDING_DIM)
    decoded_seq = dec(seq, context)

    assert get_tensor_shape(decoded_seq) == DATA_SHAPE