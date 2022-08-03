import pytest
from utils.preprocessing.text.ngram import generate_ngram


@pytest.mark.parametrize(
    "words,n",
    [
        (["text", "to", "concat"], 0),
        (["text", "to", "concat"], -1),
        (["text", "to", "concat"], -10),
    ],
)
def test_handle_error_if_n_is_less_than_one(words, n):
    with pytest.raises(ValueError):
        n_grams = generate_ngram(words, n)


@pytest.mark.parametrize(
    "words,n,ngram",
    [
        (["a"], 1, [("a",)]),
        (["a"], 2, [("a",)]),
        (["a", "b", "c"], 1, [("a",), ("b",), ("c",)]),
        (["a", "b", "c"], 2, [("a", "b"), ("b", "c")]),
        (["a", "b", "c"], 3, [("a", "b", "c")]),
        (["a", "b", "c"], 4, [("a", "b", "c")]),
    ],
)
def test_n_gram_function(words, n, ngram):
    assert generate_ngram(words, n) == ngram


@pytest.mark.parametrize(
    "words,n,ngram",
    [
        (["a"], 1, ["a"]),
        (["a"], 2, ["a"]),
        (["a", "b", "c"], 1, ["a", "b", "c"]),
        (["a", "b", "c"], 2, ["ab", "bc"]),
        (["a", "b", "c"], 3, ["abc"]),
        (["a", "b", "c"], 4, ["abc"]),
    ],
)
def test_n_gram_function_enable_concatenate(words, n, ngram):
    assert generate_ngram(words, n, concatenate=True) == ngram
