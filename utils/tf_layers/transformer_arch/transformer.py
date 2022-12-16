# reference
# https://keras.io/examples/nlp/text_classification_with_transformer/
# https://www.tensorflow.org/text/tutorials/transformer
# Attention is All You Need (Vaswani et al)

import tensorflow as tf
from tensorflow import keras
from .attention import CrossAttentionBlock, SelfAttentionBlock, MaskedSelfAttentionBlock

NUM_HEADS = 8


class TransformerEncoder(keras.layers.Layer):

    def __init__(self, embedding_dim, num_heads=NUM_HEADS, ff_nn=None):
        super().__init__()

        self.attention_block = SelfAttentionBlock(num_heads=num_heads, key_dim=embedding_dim)

        if ff_nn is None:
            self.ff_nn = keras.models.Sequential([keras.layers.Dense(32, activation='relu')])
        else:
            self.ff_nn = ff_nn

        self.attention_dense = keras.layers.Dense(embedding_dim)
        self.tfm_layernorm = keras.layers.LayerNormalization()

    def get_config(self):
        config = super().get_config()
        return config

    def call(self, x):
        # perform self-attention mechanism
        x = self.attention_block(x)

        # add non-liearity; residual connection
        dense_out = self.ff_nn(x)
        dense_out = self.attention_dense(dense_out)
        x = self.tfm_layernorm(x + dense_out)

        return x


class TransformerDecoder(keras.layers.Layer):

    def __init__(self, embedding_dim, num_heads=NUM_HEADS, ff_nn=None):
        super().__init__()
        self.masked_attention_block = MaskedSelfAttentionBlock(num_heads=num_heads,
                                                               key_dim=embedding_dim)
        self.cross_attention_block = CrossAttentionBlock(num_heads=num_heads, key_dim=embedding_dim)

        if ff_nn is None:
            self.ff_nn = keras.models.Sequential([keras.layers.Dense(32, activation='relu')])
        else:
            self.ff_nn = ff_nn
        self.attention_dense = keras.layers.Dense(embedding_dim)

        self.tfm_layernorm = keras.layers.LayerNormalization()

    def get_config(self):
        config = super().get_config()
        return config

    def call(self, x, context):
        x = self.masked_attention_block(x)
        x = self.cross_attention_block(x=x, context=context)

        self.attn_scores = self.cross_attention_block.attn_scores

        dense_out = self.ff_nn(x)
        dense_out = self.attention_dense(dense_out)
        x = self.tfm_layernorm(x + dense_out)

        return x