import altair as alt
import pandas as pd
from altair.vegalite.v4.api import Chart

from src.lib.twitter_data import TwitterData


class TwitterDataPlotter:
    def __init__(self, twitter_data: TwitterData):
        self.__twitter_data = twitter_data

    def followers_following_bar_plot(self) -> Chart:
        followers = self.__twitter_data.followers_count()
        following = self.__twitter_data.following_count()

        chart_data = pd.DataFrame(
            {"Type": ["Followers", "Following"], "Count": [followers, following]}
        )

        return (
            alt.Chart(chart_data)
            .mark_bar()
            .encode(
                alt.Y("Type", type="nominal", title=None),
                alt.X("Count", type="quantitative", title=None),
            )
        )

    def recent_tweets_metrics_plot(self) -> Chart:
        recent_tweets = self.__twitter_data.recent_tweets()
        return TwitterDataPlotter.__tweets_metrics_plot(
            recent_tweets, "Recent Tweets' metrics"
        )

    def recent_replies_metrics_plot(self) -> Chart:
        recent_replies = self.__twitter_data.recent_replies()
        return TwitterDataPlotter.__tweets_metrics_plot(
            recent_replies, "Recent replies' metrics"
        )

    @staticmethod
    def __tweets_metrics_plot(tweets: list[dict], title: str) -> Chart:
        chart_data = TwitterDataPlotter.__convert_tweets(tweets)

        return (
            alt.Chart(chart_data, title=title)
            .transform_fold(["Likes", "Retweets", "Replies"])
            .mark_line(point=True)
            .encode(
                alt.X("Date", type="temporal", title=" "),
                alt.Y("value", type="quantitative", title=None),
                alt.Color("key", type="nominal", title=None),
                tooltip=["Tweet:N", "key:N", "value:Q"],
            )
        )

    @staticmethod
    def __convert_tweets(tweets) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Date": [tweet["created_at"] for tweet in tweets],
                "Likes": [tweet["likes"] for tweet in tweets],
                "Retweets": [tweet["retweets"] for tweet in tweets],
                "Replies": [tweet["replies"] for tweet in tweets],
                "Tweet": [tweet["text"] for tweet in tweets],
            }
        )
