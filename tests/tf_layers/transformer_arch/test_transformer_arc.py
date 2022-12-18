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
from utils.tf_layers.transformer_arch.transformer import TransformerEncoder

TEST_PATH = os.path.dirname(__file__)

SEQ_LENGTH = 128
EMBEDDING_DIM = 32
BATCH_SIZE = 4
MAX_TOKENS = 1024
DATA_SHAPE = (BATCH_SIZE, SEQ_LENGTH, EMBEDDING_DIM)
TFM_HEAD = 4


def get_tensor_shape(tensor):
    return tuple(tensor.shape)


@pytest.fixture
def seq():
    sequence = np.random.randint(low=0, high=MAX_TOKENS, size=(BATCH_SIZE, SEQ_LENGTH))
    return sequence


def test_whether_mask_pass_through_layers(seq):
    em_layer = Embedding(input_dim=MAX_TOKENS, output_dim=EMBEDDING_DIM, mask_zero=True)
    pos_layer = FixedPositionalEncoding(SEQ_LENGTH, EMBEDDING_DIM)
    tfm_e = TransformerEncoder(EMBEDDING_DIM, num_heads=TFM_HEAD)

    em_seq = em_layer(seq)
    mask1 = em_seq._keras_mask
    pos_seq = pos_layer(em_seq)
    mask2 = pos_seq._keras_mask
    tfm_seq = tfm_e(pos_seq)
    mask3 = tfm_seq._keras_mask