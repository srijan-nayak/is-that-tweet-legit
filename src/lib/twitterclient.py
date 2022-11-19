import requests


class TwitterClient:
    __API_ROOT = "https://api.twitter.com/2"
    __TWEETS_ENDPOINT = f"{__API_ROOT}/tweets"
    __USERS_ENDPOINT = f"{__API_ROOT}/users"

    def __init__(self, bearer_token: str):
        self.__headers = {"Authorization": f"Bearer {bearer_token}"}

    def get_tweet_details(self, tweet_id: str) -> dict:
        tweet_fields = ",".join(["author_id"])
        return requests.get(f"{self.__TWEETS_ENDPOINT}/{tweet_id}",
                            params={"tweet.fields": tweet_fields},
                            headers=self.__headers).json()["data"]
