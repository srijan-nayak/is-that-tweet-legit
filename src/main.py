from os import environ as env

import streamlit as st
from dotenv import load_dotenv

from lib.twitter_client import TwitterClient
from lib.twitter_data import TwitterData
from src.lib.twitter_data_plotter import TwitterDataPlotter


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
        user_id, ["public_metrics", "created_at"]
    )
    all_details["user"] = user_details_response["data"]

    return all_details


if __name__ == "__main__":
    st.set_page_config(page_title="Is that Tweet legit?")

    """
    # Is that Tweet legit?
    """

    load_dotenv()
    twitter_client = TwitterClient(env["BEARER_TOKEN"])

    data = TwitterData(
        get_all_details(
            "https://twitter.com/shanselman/status/1595964315785662464", twitter_client
        )
    )

    data_plotter = TwitterDataPlotter(data)

    st.write(data.all())

    """
    ## Followers vs Following Count
    
    Accounts that follow a lot (over thousands) of people but have few followers are generally considered to be
    low-quality accounts. These type of accounts are highly likely to be spam accounts that follow a lot of people
    in an attempt to get as much attention as possible.
    """

    st.altair_chart(data_plotter.followers_following_bar(), use_container_width=True)

    """
    ## Number of updates
    
    Accounts with large numbers of followers and following will usually have a significant number of comparable updates.
    If such an account has very less tweets and the account is not that recognizable, then the account is probably a
    spam account.
    """

    updates_columns = st.columns(3)
    updates_columns[0].metric("Tweet Count", data.tweet_count())
    updates_columns[1].metric("Followers Count", data.followers_count())
    updates_columns[2].metric("Following Count", data.following_count())
