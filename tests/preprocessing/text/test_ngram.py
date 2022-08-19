import pytest
from utils.preprocessing.text.ngram import NGram


def test_initialise_ngram_helper():
    n_gram = NGram(5)
