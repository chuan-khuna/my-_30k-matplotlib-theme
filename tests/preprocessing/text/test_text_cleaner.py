from utils.preprocessing.text.text_cleaner import TextCleaner
from utils.preprocessing.text.vocabulary import Vocabulary
import pytest
from unittest.mock import patch, MagicMock, Mock

################################
# regex note
################################
# \n, \r \t = white space
# \u200b-\u200c = zero-width white space
# urls
# https://regex101.com/r/hG9t0Q/1
# https://regexr.com/3e6m0
# https://regexr.com/37i6s


@pytest.fixture
def cleaner():
    cleaner = TextCleaner()
    yield cleaner
    del cleaner


def test_initialise_obj_without_any_problems(cleaner):
    assert isinstance(cleaner, TextCleaner)


def test_default_attributes(cleaner):
    assert cleaner.remove_punctuations == True


def test_set_attributes(cleaner):
    cleaner.remove_punctuations = False
    assert cleaner.remove_punctuations == False


def test_replace_white_space_regex(cleaner):
    # special white spaces: \n, \t, \r, \u200b, \u200c, etc
    text = "text\nwith\rspecial\u200b\u200cwhite spaces\t"
    expected_text = "text with special  white spaces "
    assert cleaner._replace_special_white_spaces(text) == expected_text


def test_replace_duplicated_spaces(cleaner):
    text = "text  with  duplicated spaces"
    expected_text = "text with duplicated spaces"
    assert cleaner._replace_duplicated_spaces(text) == expected_text


def test_replace_starting_and_ending_space(cleaner):
    text = "  text with starting and ending spaces "
    expected_text = "text with starting and ending spaces"
    assert cleaner._replace_start_end_spaces(text) == expected_text


def test_replace_urls(cleaner):
    texts_with_urls = [
        "https://www.google.co.th/",
        "https://github.com/PyThaiNLP/pythainlp ",
    ]
    cleaned_texts = []
    expected_cleaned_texts = ["", " "]
    for text in texts_with_urls:
        cleaned_texts.append(cleaner._remove_urls(text))

    assert cleaned_texts == expected_cleaned_texts


def test_clean_punctuations(cleaner):
    text = "!text |with &punctuations!@#$%^&"
    expected_text = "text with punctuations"
    assert cleaner._remove_punctuations(text) == expected_text


# putting things together for clean function
def test_cleaned_text_should_not_contain_leading_and_ending_spaces(cleaner):
    expected = "text to clean"
    assert cleaner.clean(f"  {expected}  ") == expected
    assert cleaner.clean(f"\n{expected}\n") == expected
    assert cleaner.clean(f"\t{expected}\t") == expected
    assert cleaner.clean(f"\n\t{expected}\t\n") == expected


def test_cleaned_text_should_not_contain_multiple_spaces_inside(cleaner):
    assert cleaner.clean("text\t\nto \t \r\nclean") == "text to clean"


def test_clean_punct(cleaner):
    # puctuations should be cleaned at the last step
    # So it will not have an effect with some regex patters eg urls, account
    text = "  !text \r\nto \t\t clean with~ 'punctuat_ions!'*() @userid p@ssw0rd"
    expected = "text to clean with punctuations userid pssw0rd"
    assert cleaner.clean(text) == expected
    cleaner.remove_punctuations = False
    assert (
        cleaner.clean(text)
        == "!text to clean with~ 'punctuat_ions!'*() @userid p@ssw0rd"
    )


def test_clean_punct_if_it_is_set_to_false(cleaner):
    text = "text! with punc+"
    cleaner.remove_punctuations = False
    assert cleaner.clean(text) == text


def test_the_final_cleaned_text_should_not_contain_duplicate_spaces(cleaner):
    text = "! this ! is ! https://www.google.co.th/ google! \n\n url !"
    assert cleaner.clean(text) == "this is google url"
