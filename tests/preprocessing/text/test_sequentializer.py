import pytest
from utils.preprocessing.text.sequentializer import Sequentializer
from utils.preprocessing.text.sequentializer import Sequentialiser

OOV_TOKEN = "<OOV>"


@pytest.fixture
def sequentializer():

    sequentializer = Sequentializer()
    return sequentializer


def test_initialise_an_object_without_problems():
    # whether Sequentializer or Sequentialiser must be identical
    sequentializer = Sequentializer()
    sequentialiser = Sequentialiser()
    assert sequentializer.oov_token == OOV_TOKEN
    assert sequentializer.vocab is None
    assert sequentializer.inverse_vocab is None
    assert sequentializer.stopwords is None
    assert sequentializer.drop_stopwords == True


def test_inverse_should_be_protected(sequentializer):
    with pytest.raises(AttributeError):
        sequentializer.inverse_vocab = {1: OOV_TOKEN, 2: "try to set inverse vocab"}


@pytest.mark.parametrize("vocab,inverse_vocab", [({"a": 1, "b": 2}, {1: "a", 2: "b"})])
def test_set_vocab(sequentializer, vocab, inverse_vocab):
    sequentializer.vocab = vocab
    assert sequentializer.inverse_vocab == inverse_vocab


@pytest.fixture
def words_and_stopwords():
    return ["a", "b", "c", "d"], ["a", "c"], ["b", "d"]


@pytest.fixture
def vocab_and_inverse_vocab():
    return {"a": 1, "b": 2, "c": 3, "d": 4}, {1: "a", 2: "b", 3: "c", 4: "d"}


@pytest.fixture
def vocab_and_inverse_vocab_with_oov():
    return {OOV_TOKEN: 1, "a": 2, "b": 3, "c": 4, "d": 5}, {
        1: OOV_TOKEN,
        2: "a",
        3: "b",
        4: "c",
        5: "d",
    }


def test_remove_stopwords_should_do_nothing_if_stopwords_is_none(
    sequentializer, words_and_stopwords
):
    texts, stop_words, texts_no_stopwords = words_and_stopwords
    # default value of stop words is none
    # do nothing
    sequentializer.stopwords = None
    assert sequentializer.stopwords is None
    assert sequentializer.remove_stopwords(texts) == texts


def test_remove_stopwords_should_do_nothing_if_drop_stopwords_is_false(
    sequentializer, words_and_stopwords
):
    texts, stop_words, texts_no_stopwords = words_and_stopwords
    sequentializer.drop_stopwords = False
    assert sequentializer.drop_stopwords == False
    assert sequentializer.remove_stopwords(texts) == texts


@pytest.mark.parametrize(
    "input,drop_stopwords,stopwords,expected",
    [
        (["a", "b", "c", "d"], True, ["a", "c"], ["b", "d"]),
        (["a", "b", "c", "d"], False, ["a", "c"], ["a", "b", "c", "d"]),
        (["a", "b", "c", "d"], True, [], ["a", "b", "c", "d"]),
        (["a", "b", "c", "d"], True, None, ["a", "b", "c", "d"]),
        (["a", "b", "c", "d"], False, [], ["a", "b", "c", "d"]),
        (["a", "b", "c", "d"], False, None, ["a", "b", "c", "d"]),
    ],
)
def test_remove_stopwords_attributes_combinations(
    sequentializer, input, drop_stopwords, stopwords, expected
):
    # set attributes
    sequentializer.drop_stopwords = drop_stopwords
    sequentializer.stopwords = stopwords
    # clean
    assert sequentializer.remove_stopwords(input) == expected


def test_oov_tokens(sequentializer):
    # if oov token is set
    # when a word is not found in vocabulary
    # it will find for oov instead
    sequentializer.oov_token = OOV_TOKEN
    sequentializer.vocab = {OOV_TOKEN: 1}
    assert sequentializer._get_oov_token_from_dict(sequentializer.vocab) == 1
    # if oov token is not in vocab it should return None
    # for skipping mapping it from word to index
    sequentializer.vocab = {"a": 1}
    assert sequentializer._get_oov_token_from_dict(sequentializer.vocab) == None


@pytest.mark.parametrize(
    "words,vocab_dict,oov_token,values",
    [
        (["a", "b"], {"a": 1, "b": 2}, OOV_TOKEN, [1, 2]),
        (["a", "b", "c"], {"a": 1, "b": 2}, OOV_TOKEN, [1, 2]),
        (["a", "b", "c"], {OOV_TOKEN: 1, "a": 2, "b": 3}, OOV_TOKEN, [2, 3, 1]),
        (["a", "b", "c"], {OOV_TOKEN: 1, "a": 2, "b": 3}, None, [2, 3]),
    ],
)
def test_mapping_keys_to_values(sequentializer, words, vocab_dict, oov_token, values):
    sequentializer.oov_token = oov_token
    assert sequentializer._map_keys_to_values(words, vocab_dict) == values


def test_helper_function_to_convert_keys_to_vals(
    sequentializer, vocab_and_inverse_vocab_with_oov, vocab_and_inverse_vocab
):
    words = ["a", "b", "f", "c", "d", "e"]
    v1, iv1 = vocab_and_inverse_vocab
    v2, iv2 = vocab_and_inverse_vocab_with_oov
    sequentializer.vocab = v1
    assert sequentializer._map_keys_to_values(words, sequentializer.vocab) == [
        1,
        2,
        3,
        4,
    ]
    sequentializer.vocab = v2
    assert sequentializer._map_keys_to_values(words, sequentializer.vocab) == [
        2,
        3,
        1,
        4,
        5,
        1,
    ]


@pytest.mark.parametrize("vocab", [None])
def test_convert_text_to_sequence_should_raise_error_if_vocab_not_set(
    sequentializer, vocab
):
    with pytest.raises(ValueError):
        sequentializer.vocab = vocab
        sequentializer.text_to_sequence(["a", "b"])


@pytest.mark.parametrize(
    "vocab,oov,text,sequence",
    [
        ({"a": 1, "b": 2}, OOV_TOKEN, ["a", "b", "c"], [1, 2]),
        ({OOV_TOKEN: 1, "a": 2, "b": 3}, OOV_TOKEN, ["a", "b", "c"], [2, 3, 1]),
        ({OOV_TOKEN: 1, "a": 2, "b": 3}, None, ["a", "b", "c"], [2, 3]),
        ({}, None, ["a", "b", "c"], []),
        ({}, OOV_TOKEN, ["a", "b", "c"], []),
    ],
)
def test_convert_text_to_sequence(sequentializer, vocab, text, oov, sequence):
    sequentializer.vocab = vocab
    sequentializer.oov_token = oov
    assert sequentializer.text_to_sequence(text) == sequence
    # easter egg
    assert sequentializer.sequentialize(text) == sequence
    assert sequentializer.sequentialise(text) == sequence


@pytest.mark.parametrize(
    "vocab,oov,sequence,text",
    [
        ({"a": 1, "b": 2}, OOV_TOKEN, [1, 2], ["a", "b"]),
        ({"a": 1, "b": 2}, OOV_TOKEN, [1, 2, 3], ["a", "b"]),
        ({OOV_TOKEN: 1, "a": 2, "b": 3}, OOV_TOKEN, [2, 3, 1], ["a", "b", OOV_TOKEN]),
        ({OOV_TOKEN: 1, "a": 2, "b": 3}, None, [2, 3, 1], ["a", "b", OOV_TOKEN]),
        ({}, None, [1, 2, 3], []),
        ({}, OOV_TOKEN, [1, 2, 3], []),
    ],
)
def test_convert_sequence_to_text(sequentializer, vocab, text, oov, sequence):
    sequentializer.vocab = vocab
    sequentializer.oov_token = oov
    assert sequentializer.sequence_to_text(sequence) == text
    # easter egg
    assert sequentializer.desequentialize(sequence) == text
    assert sequentializer.desequentialise(sequence) == text
