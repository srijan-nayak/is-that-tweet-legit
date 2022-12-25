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
        """Returns the followers count if available. Returns -1 otherwise."""
        try:
            return self.__data["user"]["public_metrics"]["followers_count"]
        except KeyError:
            return -1

    def following_count(self) -> int:
        """Returns the following count if available. Returns -1 otherwise."""
        try:
            return self.__data["user"]["public_metrics"]["following_count"]
        except KeyError:
            return -1

    def tweet_count(self) -> int:
        """Returns the tweet count if available. Returns -1 otherwise."""
        try:
            return self.__data["user"]["public_metrics"]["tweet_count"]
        except KeyError:
            return -1

    def account_age(self) -> int:
        """Returns the age of account in days if created at time is available. Returns -1 otherwise."""
        try:
            created_at = parse(self.__data["user"]["created_at"])
            time_delta = datetime.now(timezone.utc) - created_at
            return time_delta.days
        except KeyError:
            return -1
