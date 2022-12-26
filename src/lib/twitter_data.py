from datetime import datetime, timezone

from dateutil.parser import parse


class TwitterData:
    """
    Model containing fetched Twitter data.

    Provides methods to easily extract useful information.
    """

    def __init__(self, data: dict):
        self.__data = data

    def all(self):
        """Returns a copy of the entire data."""
        return self.__data.copy()

    def followers_count(self) -> int:
        """Returns the followers count if available."""
        return self.__data["user"]["public_metrics"]["followers_count"]

    def following_count(self) -> int:
        """Returns the following count if available."""
        return self.__data["user"]["public_metrics"]["following_count"]

    def tweet_count(self) -> int:
        """Returns the tweet count if available."""
        return self.__data["user"]["public_metrics"]["tweet_count"]

    def account_age(self) -> int:
        """Returns the age of account in days if created at time is available."""
        created_at = parse(self.__data["user"]["created_at"])
        time_delta = datetime.now(timezone.utc) - created_at
        return time_delta.days

    def recent_tweets(self) -> list[dict]:
        """Fetches recent tweets from the account."""
        tweets = self.__data["tweets"]
        return [TwitterData.__transform_tweet_data(data) for data in tweets]

    def recent_replies(self) -> list[dict]:
        """Fetches recent replies from the account."""
        reply_tweets = self.__data["reply_tweets"]
        return [TwitterData.__transform_tweet_data(data) for data in reply_tweets]

    @staticmethod
    def __transform_tweet_data(data: dict) -> dict:
        return {
            "created_at": parse(data["created_at"]),
            "text": data["text"],
            "retweets": data["public_metrics"]["retweet_count"],
            "replies": data["public_metrics"]["reply_count"],
            "likes": data["public_metrics"]["like_count"],
            "quotes": data["public_metrics"]["quote_count"],
        }
