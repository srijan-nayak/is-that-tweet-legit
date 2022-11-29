from os import environ as env

import streamlit as st
from dotenv import load_dotenv

from lib.twitterclient import TwitterClient


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


# RAKSHA


# PRADEEP

# SRINIVAS

# SRIVIKA

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

    # RAKSHA

    res=data.items()
    re1=list(res)
    re2=re1[1][1]
    re3=re2.items()
    re4=list(re3)
    re5=re4[3][1]
    re6=re5.items()
    re7=list(re6)
    re8=re7[0][1]
    re9=re7[1][1]
    st.write(res)
    st.write(re1)
    st.write(re2)
    st.write(re3)
    st.write(re4)
    st.write(re5)
    st.write(re6)
    st.write(re7)
    st.write(re8)
    st.write(re9)





# PRADEEP

# SRINIVAS

# SRIVIKA
