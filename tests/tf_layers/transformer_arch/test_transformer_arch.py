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


def test_transformer_encoder(seq):
    pos_em_layer = PositionalEmbedding(vocab_size=MAX_TOKENS, embedding_dim=EMBEDDING_DIM)

    encoder_block = TransformerEncoderBlock(embedding_dim=EMBEDDING_DIM,
                                            num_heads=NUM_HEADS,
                                            dense_dim=512,
                                            dropout_rate=0.1)

    em_seq = pos_em_layer(seq)
    encoded_seq = encoder_block(em_seq)

    assert get_tensor_shape(em_seq) == DATA_SHAPE
    assert get_tensor_shape(encoded_seq) == DATA_SHAPE
    # it should be able to access self attention's attention scores
    encoder_block.attn_scores
    assert get_tensor_shape(encoder_block.attn_scores) == (BATCH_SIZE, NUM_HEADS, SEQ_LENGTH,
                                                           SEQ_LENGTH)


def test_transformer_decoder(seq):
    pos_em_layer = PositionalEmbedding(vocab_size=MAX_TOKENS, embedding_dim=EMBEDDING_DIM)

    decoder_block = TransformerDecoderBlock(embedding_dim=EMBEDDING_DIM,
                                            num_heads=NUM_HEADS,
                                            dense_dim=512,
                                            dropout_rate=0.1)

    CONTEXT_LENGTH = SEQ_LENGTH // 2

    x_seq = pos_em_layer(seq)
    context_seq = pos_em_layer(seq[:, :CONTEXT_LENGTH])

    # x, context
    decoded_seq = decoder_block(x_seq, context_seq)

    assert get_tensor_shape(x_seq) == DATA_SHAPE
    assert get_tensor_shape(decoded_seq) == DATA_SHAPE
    # it should be able to access self attention's attention scores
    decoder_block.attn_scores
    assert get_tensor_shape(decoder_block.attn_scores) == (BATCH_SIZE, NUM_HEADS, SEQ_LENGTH,
                                                           CONTEXT_LENGTH)


def test_encoder_decoder_arch(seq):

    pos_em_layer = PositionalEmbedding(vocab_size=MAX_TOKENS, embedding_dim=EMBEDDING_DIM)
    encoder_block = TransformerEncoderBlock(embedding_dim=EMBEDDING_DIM,
                                            num_heads=NUM_HEADS,
                                            dense_dim=512,
                                            dropout_rate=0.1)
    decoder_block = TransformerDecoderBlock(embedding_dim=EMBEDDING_DIM,
                                            num_heads=NUM_HEADS,
                                            dense_dim=512,
                                            dropout_rate=0.1)

    CONTEXT_LENGTH = SEQ_LENGTH // 2

    x = pos_em_layer(seq)
    context = pos_em_layer(seq[:, :CONTEXT_LENGTH])

    context = encoder_block(context)
    x = decoder_block(x, context)