from os import environ as env

import streamlit as st
from dotenv import load_dotenv

from lib.twitterclient import TwitterClient


@st.cache
def get_all_details(tweet_url_or_id: str, twitter_client: TwitterClient) -> dict:
    all_details = {}

    tweet_id = tweet_url_or_id.split("/")[-1]
    tweet_details_response = twitter_client.fetch_tweet_details(tweet_id, ["public_metrics", "author_id"])
    all_details["tweet"] = tweet_details_response["data"]

    user_id = all_details["tweet"]["author_id"]
    user_details_response = twitter_client.fetch_user_details(user_id, ["public_metrics"])
    all_details["user"] = user_details_response["data"]

    return all_details


load_dotenv()
BEARER_TOKEN = env["BEARER_TOKEN"]

if __name__ == '__main__':
    st.write("# Is that Tweet legit?")
