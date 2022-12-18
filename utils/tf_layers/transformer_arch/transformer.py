# reference
# https://keras.io/examples/nlp/text_classification_with_transformer/
# https://www.tensorflow.org/text/tutorials/transformer
# Attention is All You Need (Vaswani et al)

import tensorflow as tf
from tensorflow import keras
from .attention import CrossAttentionBlock, SelfAttentionBlock, MaskedSelfAttentionBlock

NUM_HEADS = 8


class TransformerEncoder(keras.layers.Layer):

    def __init__(self, embedding_dim, num_heads=NUM_HEADS, ff_nn=None, dropout_rate=0.1):
        super().__init__()

        self.attention_block = SelfAttentionBlock(num_heads=num_heads,
                                                  key_dim=embedding_dim,
                                                  dropout=dropout_rate)

        # feed-forward block at the top of attention
        # to add non-linearity and produce an output as the same shape of the input
        if ff_nn is None:
            self.ff_nn = keras.models.Sequential([keras.layers.Dense(32, activation='relu')])
        else:
            self.ff_nn = ff_nn
        self.dense = keras.layers.Dense(embedding_dim)
        self.dropout = keras.layers.Dropout(0.1)

        self.residual_add = keras.layers.Add()
        self.tfm_layernorm = keras.layers.LayerNormalization()

    def get_config(self):
        config = super().get_config()
        return config

    def call(self, x):
        # perform self-attention mechanism
        x = self.attention_block(x)
        self.attn_scores = self.attention_block.attn_scores

        # add non-liearity; residual connection
        dense_out = self.ff_nn(x)
        dense_out = self.dense(dense_out)
        dense_out = self.dropout(dense_out)
        x =  self.residual_add([x, dense_out])
        x = self.tfm_layernorm(x)

        return x


class TransformerDecoder(keras.layers.Layer):

    def __init__(self, embedding_dim, num_heads=NUM_HEADS, ff_nn=None, dropout_rate=0.1):
        super().__init__()
        self.masked_attention_block = MaskedSelfAttentionBlock(num_heads=num_heads,
                                                               key_dim=embedding_dim,
                                                               dropout=dropout_rate)
        self.cross_attention_block = CrossAttentionBlock(num_heads=num_heads,
                                                         key_dim=embedding_dim,
                                                         dropout=dropout_rate)

        # feed-forward block at the top of attention
        # to add non-linearity and produce an output as the same shape of the input
        if ff_nn is None:
            self.ff_nn = keras.models.Sequential([keras.layers.Dense(32, activation='relu')])
        else:
            self.ff_nn = ff_nn
        self.dense = keras.layers.Dense(embedding_dim)
        self.dropout = keras.layers.Dropout(0.1)

        self.residual_add = keras.layers.Add()
        self.tfm_layernorm = keras.layers.LayerNormalization()

    def get_config(self):
        config = super().get_config()
        return config

    def call(self, x, context):
        # perform masked-self-attention mechanism
        x = self.masked_attention_block(x)
        x = self.cross_attention_block(x=x, context=context)

        self.attn_scores = self.cross_attention_block.attn_scores

        # add non-liearity; residual connection
        dense_out = self.ff_nn(x)
        dense_out = self.dense(dense_out)
        dense_out = self.dropout(dense_out)

        x =  self.residual_add([x, dense_out])
        x = self.tfm_layernorm(x)

        return x