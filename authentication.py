
import configparser
from tweepy import OAuthHandler

class TwitterAuthenticator():
    """
    Twitter Authenticater
    """
    def authontication_twitter_app(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        api_key = config['twitter']['api_key']
        api_key_secret = config['twitter']['api_key_secret']
        access_token = config['twitter']['access_token']
        access_token_secret = config['twitter']['access_token_secret']
        auth = OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth