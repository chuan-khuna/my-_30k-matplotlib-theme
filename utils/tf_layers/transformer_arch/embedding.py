# ref: https://machinelearningmastery.com/the-transformer-positional-encoding-layer-in-keras-part-2/
# https://www.tensorflow.org/text/tutorials/transformer#the_embedding_and_positional_encoding_layer

# don't forget to add mask_zero at the Embedding layer
# preprocessing token to vector - https://www.tensorflow.org/api_docs/python/tf/keras/layers/TextVectorization
# Embedding masking - https://www.tensorflow.org/text/tutorials/transformer#the_embedding_and_positional_encoding_layer
# evaluation metrics - https://www.tensorflow.org/text/tutorials/transformer#set_up_the_loss_and_metrics
# RNN + Embedding Use masking to handle the variable sequence lengths -  https://www.tensorflow.org/text/tutorials/text_classification_rnn
# https://www.tensorflow.org/guide/keras/masking_and_padding

import tensorflow as tf
from tensorflow import keras
import numpy as np


class FixedPositionalEncoding(keras.layers.Layer):
    """Add "Positional Encodings" to embedding vectors

    How to use:

    model.add(Embedding(..., mask_zero=True))
    model.add(FixedPositionalEncoding(....))

    Ref: Attention is All You Need (Vaswani et al)

    Args:
        keras (_type_): _description_
    """

    def __init__(self, seq_length: int, embed_dim: int, n: int = 10000):
        super().__init__()

        self.embed_dim = embed_dim

        # create layer with fixed weights
        positional_encoding_weights = self.__get_embedding_matrix(seq_length, embed_dim, n)
        self.position_encoding_layer = tf.keras.layers.Embedding(
            input_dim=seq_length,
            output_dim=embed_dim,
            weights=[positional_encoding_weights],
            trainable=False)

        self.add = keras.layers.Add()

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
        seq_length = tf.shape(x)[1]

        positions = tf.range(start=0, limit=seq_length, delta=1)
        pos_encoding = self.position_encoding_layer(positions)
        pos_encoding = pos_encoding[tf.newaxis, :seq_length, :]

        # scaling
        # x *= tf.math.sqrt(tf.cast(self.embed_dim, tf.float32))

        x = x + pos_encoding
        return x