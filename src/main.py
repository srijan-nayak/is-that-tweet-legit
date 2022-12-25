from os import environ as env

import streamlit as st
from dotenv import load_dotenv

from src.lib.twitter_client import TwitterClient
from src.lib.twitter_data import TwitterData
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
    all_details["tweet"] = tweet_details_response.get("data", {})

    user_id = all_details["tweet"].get("author_id", "invalid")
    user_details_response = twitter_client.fetch_user_details(
        user_id, ["public_metrics", "created_at"]
    )
    all_details["user"] = user_details_response.get("data", {})

    user_name = all_details["user"].get("username", "")
    reply_tweets_response = twitter_client.fetch_reply_tweets(user_name)
    all_details["reply_tweets"] = reply_tweets_response.get("data", {})

    return all_details


if __name__ == "__main__":
    st.set_page_config(page_title="Is that Tweet legit?")

    """
    # Is that Tweet legit?
    """

    load_dotenv()
    twitter_client = TwitterClient(env["BEARER_TOKEN"])

    can_show_details = False
    with st.form("twitter_link_form"):
        tweet_url_or_id = st.text_input("Tweet link or URL")
        submitted = st.form_submit_button("Fetch data")

        if submitted:
            try:
                data = TwitterData(get_all_details(tweet_url_or_id, twitter_client))
                data_plotter = TwitterDataPlotter(data)
                can_show_details = True
            except KeyError:
                st.error("Failed to fetch data!")

    if can_show_details:
        st.json(data.all())

        """
        ## Followers vs Following Count
        """

        try:
            st.altair_chart(
                data_plotter.followers_following_bar(), use_container_width=True
            )

            followers_following_columns = st.columns(2)
            followers_following_columns[0].metric("Followers", data.followers_count())
            followers_following_columns[1].metric("Following", data.following_count())
        except KeyError:
            st.error("Failed to fetch followers and following information!")

        """
        Accounts that follow a lot (over thousands) of people but have few followers are generally considered to be
        low-quality accounts. These type of accounts are highly likely to be spam accounts that follow a lot of people
        in an attempt to get as much attention as possible.
        """

        updates_column, age_column = st.columns(2)

        with updates_column:
            """
            ## Number of updates
            """

            try:
                st.metric("Tweet Count", data.tweet_count())
            except KeyError:
                st.error("Failed to fetch Tweet count!")

            """
            If an account with large followers and following has very less tweets and the account is not that
            recognizable, then the account is probably a spam account.
            """

        with age_column:
            """
            ## Age of account
            """

            try:
                st.metric("Account age in days", data.account_age())
            except KeyError:
                st.error("Failed to fetch 'created at' information!")

            """
            An account that is not so recognizable but has large number of followers and following in a short period of
            time is another indicator for a spam account.
            """
