# reference
# https://keras.io/examples/nlp/text_classification_with_transformer/
# Ref: Attention is All You Need (Vaswani et al)

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, MultiHeadAttention


class TransformerBlock(keras.layers.Layer):
    """A Transformer Block with multi-headed self-attention

    - multi-headed self-attention, ie q, k, v are the same

    Ref: Attention is All You Need (Vaswani et al)

    How to use:

    Embedding()
    TransformerBlock() -> shape: batch, seq_length, embedding_dim

    Args:
        keras (_type_): _description_
    """

    def __init__(self, embedding_dim: int, num_heads: int = 6, ff_nn=None):
        """A Transformer Block

        Args:
            embedding_dim (int): _description_
            num_heads (int, optional): _description_. Defaults to 6.
            ff_nn (_type_, optional): `Sequential` model with dense layers `[Dense, Dense, ...]` for adding non-linearity to the Transformer output; `ff_nn` doesn't have to consist the last `Dense(embedding_dim)`
            Defaults to None (add one Dense(32, relu)).
        """
        super(TransformerBlock, self).__init__()

        self.attention = MultiHeadAttention(num_heads=num_heads, key_dim=embedding_dim)
        self.layer_norm1 = keras.layers.LayerNormalization(epsilon=1e-6)
        self.layer_norm2 = keras.layers.LayerNormalization(epsilon=1e-6)
        self.attention_dense = Dense(embedding_dim)

        if ff_nn is None:
            self.ff_nn = keras.models.Sequential([Dense(32, activation='relu')])
        else:
            self.ff_nn = ff_nn

    def get_config(self):
        config = super().get_config()
        return config

    def call(self, inputs):
        """_summary_

        Args:
            inputs (_type_): vectors from embedding-like layer, eg Embedding, Conv1D

        Returns:
            _type_: _description_
        """

        # perform self-attention mechanism: query, key, value are the same
        attention_out = self.attention(inputs, inputs)
        # residual connection
        attention_out = self.layer_norm1(inputs + attention_out)

        # add non-linearity and residual connection
        dense_out = self.ff_nn(attention_out)
        dense_out = self.attention_dense(dense_out)
        out = self.layer_norm2(inputs + dense_out)

        # shape: batch_size, sequence_length, embedding_dim
        return out