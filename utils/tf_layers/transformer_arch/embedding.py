# ref: https://machinelearningmastery.com/the-transformer-positional-encoding-layer-in-keras-part-2/

import tensorflow as tf
from tensorflow import keras
import numpy as np


class FixedPositionalEncoding(keras.layers.Layer):
    """Add "Positional Encodings" to embedding vectors

    How to use:

    model.add(Embedding(...))
    model.add(FixedPositionalEncoding(....))

    Ref: Attention is All You Need (Vaswani et al)

    Args:
        keras (_type_): _description_
    """

    def __init__(self, seq_length: int, embed_dim: int, n: int = 10000):
        super(FixedPositionalEncoding, self).__init__()

        # create layer with fixed weights
        positional_encoding_weights = self.__get_embedding_matrix(seq_length, embed_dim, n)
        self.position_encoding_layer = tf.keras.layers.Embedding(
            input_dim=seq_length,
            output_dim=embed_dim,
            weights=[positional_encoding_weights],
            trainable=False)

    def get_config(self):
        config = super().get_config()
        return config

    def __get_embedding_matrix(self, seq_length: int, embed_dim: int, n: int) -> np.array:
        pos_embedding = np.zeros((seq_length, embed_dim))

        dim_arr = np.arange(0, embed_dim)
        even_mask = np.array(dim_arr % 2 == 0, int)
        odd_mask = np.array(dim_arr % 2 != 0, int)

        # calculate embedding for position i
        for pos_i in range(seq_length):
            even_emb = np.sin(pos_i / n**(2 * dim_arr / embed_dim)) * even_mask
            odd_emb = np.cos(pos_i / n**(2 * dim_arr / embed_dim)) * odd_mask
            pos_embedding[pos_i] = even_emb + odd_emb

        return pos_embedding

    def call(self, x):
        """_summary_

        Args:
            x (_type_): `x` is a list of embedding vectors, ie `(seq length, embedding dim)`

        Returns:
            _type_: x + positional encodings
        """
        seq_length = tf.shape(x)[-2]
        positions = tf.range(start=0, limit=seq_length, delta=1)
        pos_encoding = self.position_encoding_layer(positions)
        return x + pos_encoding