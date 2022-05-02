import tweepy
from tweepy import Cursor
from helpers.authentication import TwitterAuthenticator

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator.authontication_twitter_app(self)
        self.twitter_client = tweepy.API(self.auth, wait_on_rate_limit=True)
        self.tweeter_user = twitter_user
    
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.tweeter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.tweeter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets
    
    def get_twitter_client_api(self):
        return self.twitter_client