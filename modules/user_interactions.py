from datetime import datetime
from modules.twitter_analyzer import TweetAnalyzer
from modules.twitter_client import TwitterClient
import pytz

class UserInteraction():
    """
    Get the most interacted friends/followers in a month
    """
    def __init__(self):
        self.api = TwitterClient().get_twitter_client_api()
        self.tweet_analyzer = TweetAnalyzer()

    def get_most_interactives(self, user_name , type):
        utc = pytz.UTC
        startDate = datetime(2022, 3, 1, 0, 0, 0).replace(tzinfo=utc)
        endDate =   datetime(2022, 3, 30, 0, 0, 0).replace(tzinfo=utc)

        tweets = []

        tmpTweets = self.api.user_timeline(screen_name=user_name)

        for tweet in tmpTweets:
            if tweet.created_at.replace(tzinfo=utc) < endDate and tweet.created_at.replace(tzinfo=utc) > startDate.replace(tzinfo=utc):
                tweets.append(tweet)
        
        prev_tem_tweet = []

        while tmpTweets[-1] != prev_tem_tweet and (tmpTweets[-1].created_at.replace(tzinfo=utc) > startDate):
            prev_tem_tweet = tmpTweets[-1]
            # print(tmpTweets[-1].created_at.replace(tzinfo=utc))
            tmpTweets = self.api.user_timeline(screen_name=user_name, max_id = tmpTweets[-1].id)
            for tweet in tmpTweets:
                if tweet.created_at.replace(tzinfo=utc) < endDate and tweet.created_at > startDate:
                    tweets.append(tweet)

        df = self.tweet_analyzer.tweets_to_data_frame(tweets)
        df = df.groupby(["author", "in_reply_to_screen_name"], as_index=False)["author"].agg({'mention_count':'count'}).sort_values(by='mention_count', ascending=False)
        df = df.reset_index()
        if type == 'friend':
            df = df.head(5)
        else:
            df = df[df.mention_count>10]
        return df