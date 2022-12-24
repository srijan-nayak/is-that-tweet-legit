from os import environ as env

import streamlit as st
from dotenv import load_dotenv

from lib.twitterclient import TwitterClient
import pandas as pd


@st.cache
def get_all_details(tweet_url_or_id: str, twitter_client: TwitterClient) -> dict:
    """
    Fetches relevant information for a given Tweet URL or ID and returns it as a dictionary.

    :param tweet_url_or_id: The url or ID of the Tweet for which the details should be fetched.
    :param twitter_client: An instance of TwitterClient for making the API requests.
    :return: A dictionary containing all the data.
    """
    all_details = {}

    tweet_id = tweet_url_or_id.split("/")[-1]
    tweet_details_response = twitter_client.fetch_tweet_details(
        tweet_id, ["public_metrics", "author_id"]
    )
    all_details["tweet"] = tweet_details_response["data"]

    user_id = all_details["tweet"]["author_id"]
    user_details_response = twitter_client.fetch_user_details(
        user_id, ["public_metrics"]
    )
    all_details["user"] = user_details_response["data"]

    return all_details


def get_followers_count(twitter_data: dict) -> int:
    return twitter_data["user"]["public_metrics"]["followers_count"]


def get_following_count(twitter_data: dict) -> int:
    return twitter_data["user"]["public_metrics"]["following_count"]


if __name__ == "__main__":
    st.set_page_config(page_title="Is that Tweet legit?")

    """
    # Is that Tweet legit?
    """

    load_dotenv()
    twitter_client = TwitterClient(env["BEARER_TOKEN"])

    data = get_all_details(
        "https://twitter.com/shanselman/status/1595964315785662464", twitter_client
    )

    st.write(data)

    """
    ## Followers Count vs Following Count
    An account that follows a lot of people but has few followers is generally considered a low-quality account or may 
    even be a fake account. 
    """
    """
    
    """
    st.bar_chart(
        pd.DataFrame(
            [get_followers_count(data), get_following_count(data)],
            columns=["Count"],
            index=["Followers", "Following"],
        )
    )
