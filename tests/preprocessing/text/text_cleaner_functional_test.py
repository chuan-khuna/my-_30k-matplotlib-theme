from utils.preprocessing.text.text_cleaner import TextCleaner
from utils.preprocessing.text.vocabulary import Vocabulary
import pytest


@pytest.mark.parametrize(
    "text,punct,expected",
    [
        ("Hello", True, "Hello"),
        ("Hello", False, "Hello"),
        (" Hello world ! ", True, "Hello world"),
        (" Hello world ! ", False, "Hello world !"),
        (
            " Funct!0nal ! Tests \rof \t!\t TextCleaner\n",
            True,
            "Funct0nal Tests of TextCleaner",
        ),
    ],
)
def test_text_cleaner(text, punct, expected):
    # I have a list of text for NLP tasks
    # generated via pytest parametrized
    # I impoort my utils and initilise the obj
    cln = TextCleaner()

    # I can set whether I want remove punctuation or not
    cln.remove_punctuations = punct

    # clean texts for a tokeniser
    assert cln.clean(text) == expected

    # then I pass the cleaned texts to a tokeniser
    # tokenised_texts = [text.split(' ') for text in cleaned_texts]
    # ...
