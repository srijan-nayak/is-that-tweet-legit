import requests


class TwitterClient:
    __API_ROOT = "https://api.twitter.com/2"
    __TWEETS_ENDPOINT = f"{__API_ROOT}/tweets"
    __USERS_ENDPOINT = f"{__API_ROOT}/users"

    def __init__(self, bearer_token: str):
        self.__headers = {"Authorization": f"Bearer {bearer_token}"}

    def fetch_tweet_details(
        self, tweet_id: str, additional_fields: list[str] = None
    ) -> dict:
        tweet_fields = ",".join(additional_fields) if additional_fields else []
        return requests.get(
            f"{self.__TWEETS_ENDPOINT}/{tweet_id}",
            params={"tweet.fields": tweet_fields},
            headers=self.__headers,
        ).json()

    def fetch_user_details(
        self, user_id: str, additional_fields: list[str] = None
    ) -> dict:
        user_fields = ",".join(additional_fields) if additional_fields else []
        return requests.get(
            f"{self.__USERS_ENDPOINT}/{user_id}",
            params={"user.fields": user_fields},
            headers=self.__headers,
        ).json()
