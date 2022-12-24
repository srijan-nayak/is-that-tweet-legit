import altair as alt
import pandas as pd

from src.lib.twitter_data import TwitterData


class TwitterDataPlotter:
    def __init__(self, twitter_data: TwitterData):
        self.__twitter_data = twitter_data

    def followers_following_bar(self):
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
                alt.X("Count", type="quantitative"),
            )
        )
