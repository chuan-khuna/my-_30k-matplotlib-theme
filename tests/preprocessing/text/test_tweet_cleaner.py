from utils.preprocessing.text.tweet_cleaner import TweetCleaner
from utils.preprocessing.text.text_cleaner import TextCleaner
import pytest


@pytest.fixture
def tweet_cleaner():
    tweet_cleaner = TweetCleaner()
    yield tweet_cleaner
    del tweet_cleaner


def test_tweet_cleaner_is_inherited_from_text_cleaner():
    cleaner = TweetCleaner()
    assert isinstance(cleaner, TweetCleaner)
    assert isinstance(cleaner, TextCleaner)


def test_tweet_cleaner_default_atttributes(tweet_cleaner):
    assert tweet_cleaner.remove_punctuations == True


def test_tweet_cleaner_inherited_attributes(tweet_cleaner):
    text_cleaner = TextCleaner()
    assert tweet_cleaner.remove_punctuations == text_cleaner.remove_punctuations


def test_get_RT_user_id(tweet_cleaner):
    # RT format
    # RT @user_source: tweet content
    tweet = "RT @some_user: Hello world!"
    assert tweet_cleaner.get_RT_user(tweet) == "@some_user"

    tweet = "RT @someuser: Hello world!"
    assert tweet_cleaner.get_RT_user(tweet) == "@someuser"

    tweet = "RT @someuserwithveryloiduserud: Hello world!"
    assert tweet_cleaner.get_RT_user(tweet) == "@someuserwithveryloiduserud"

    tweet = "RT @usr: Hello world! @userASD"
    assert tweet_cleaner.get_RT_user(tweet) == "@usr"

    tweet = "No user"
    assert tweet_cleaner.get_RT_user(tweet) is None


def test_get_mentioned_users(tweet_cleaner):
    # included RT
    tweet = "RT @some_user: Hello world! @userA, @userB\n@userCwithverylongname , @usrd"
    expected_mentioned_users = [
        "@some_user",
        "@userA",
        "@userB",
        "@userCwithverylongname",
        "@usrd",
    ]
    assert tweet_cleaner.get_mentioned_users(tweet) == expected_mentioned_users

    tweet = "no user is mentioned"
    assert tweet_cleaner.get_mentioned_users(tweet) is None


def test_replace_RT_start(tweet_cleaner):
    tweet = "RT @some_user: Hello world! @userA"
    expected_cleaned_tweet = "Hello world! @userA"
    assert tweet_cleaner._replace_RT_start(tweet) == expected_cleaned_tweet


def test_replace_all_users(tweet_cleaner):
    tweet = "@userA @userB Hello World!"
    expected_cleaned_tweet = "  Hello World!"
    assert tweet_cleaner._replace_all_users(tweet) == expected_cleaned_tweet


def test_clean_method(tweet_cleaner):
    # Only tweet content
    tweet = "RT @some_user: Hello world! @userA @userB\n@userCwithverylongname  @usrd"
    expected_cleaned_tweet = "Hello world!"
    tweet_cleaner.remove_punctuations = False
    assert tweet_cleaner.remove_punctuations == False
    assert (tweet_cleaner.clean(tweet) == expected_cleaned_tweet)

    tweet_cleaner.remove_punctuations = True
    assert tweet_cleaner.remove_punctuations == True
    tweet = "RT @some_user: Hello world! @userA @userB\n@userCwithverylongname  @usrd"
    expected_cleaned_tweet = "Hello world"
    assert (tweet_cleaner.clean(tweet) == expected_cleaned_tweet)

    tweet = "RT @some_user: https://www.youtube.com/ Hello world! by @userA"
    expected_cleaned_tweet = "Hello world by"
    assert (tweet_cleaner.clean(tweet) == expected_cleaned_tweet)


def test_replace_child_method_with_parent_method_it_should_not_error(tweet_cleaner):
    # suppose that we don't know what class the obj. is
    # tweet cleaner should be able to substitute for text cleaner
    text_cleaner = TextCleaner()
    tweet = "RT @some_user: https://www.youtube.com/ Hello world! by @userA"
    text_cleaner.clean(tweet)
    tweet_cleaner.clean(tweet)
