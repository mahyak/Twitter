import pandas as pd
import numpy as np

class TweetAnalyzer():
    """
    Functionality for analyzing and categotizing content from tweets
    """
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['author'] = np.array([tweet.author.screen_name for tweet in tweets])
        df['tweet_id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['in_reply_to_screen_name'] = np.array([tweet.in_reply_to_screen_name for tweet in tweets])
        df['in_reply_to_status_id'] = np.array([tweet.in_reply_to_status_id for tweet in tweets])
        df['in_reply_to_user_id'] = np.array([tweet.in_reply_to_user_id for tweet in tweets])

        return df
