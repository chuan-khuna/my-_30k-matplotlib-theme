# My Transformer Wrapper/Utils

requirements: `python 3.10, tensorflow 2.11`

references:

- https://www.tensorflow.org/text/tutorials/transformer
- https://keras.io/examples/nlp/text_classification_with_transformer/
- https://www.youtube.com/watch?v=ptuGllU5SQQ

## Notes about the output dimensions

Suppose that I have data processed by `Embedding` layer

```py
D_MODEL = EMBEDDING_SHAPE = 32
MAX_SEQ_LENGTH = 200
MOCK_DATA = np.array([np.round(np.random.random((MAX_SEQ_LENGTH, EMBEDDING_SHAPE)), 2)])

# embedding
em = tf.constant(MOCK_DATA)
em.shape
# batch_size, seq_length, embedding_dim
```

```txt
<tf.Tensor: shape=(1, 200, 32), dtype=float64, numpy=
array([[[0.02, 0.26, 0.21, ..., 0.74, 0.39, 0.09],
        [0.57, 0.06, 0.09, ..., 0.28, 0.7 , 0.48],
        [0.56, 0.98, 0.16, ..., 0.49, 0.7 , 0.96],
        ...,
        [0.59, 0.73, 0.8 , ..., 0.6 , 0.82, 0.45],
        [0.15, 0.64, 0.63, ..., 0.21, 0.44, 0.57],
        [0.85, 0.76, 0.67, ..., 0.07, 0.49, 0.18]]])>
```

To add "Positional Encoding" -- the `sin, cos` encoding in **Attention is All You Need**

```py
pos_encoding = FixedPositionalEncoding(MAX_SEQ_LENGTH, EMBEDDING_SHAPE)
# > batch_size, seq_length, embedding_dim

# Embedding()
# FixedPositionalEncoding()
```

To use **Attention**

```py
self_att = SelfAttentionBlock(num_heads=8, key_dim=EMBEDDING_SHAPE)
cross_att = CrossAttentionBlock(num_heads=8, key_dim=EMBEDDING_SHAPE)
cross_att(em_x, em_context)
# > batch_size, seq_length, embedding_dim
```

The **Encoder-Decoder** architecture

```py
tfme = TransformerEncoder(EMBEDDING_SHAPE, num_heads=8)
tfmd = TransformerDecoder(EMBEDDING_SHAPE, num_heads=8)
cross_att(em_x, em_context)
# > batch_size, seq_length, embedding_dim
```