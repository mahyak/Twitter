from tweepy.streaming import Stream

class TwitterListener(Stream):
    """
     This is a basic listener class that just prints recieved tweets to stdout
    """
    def __init__(self, fetched_tweet_filename):
        self.fetched_tweet_filename = fetched_tweet_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweet_filename, 'a') as tf:
                tf.write(data)
        except BaseException as e:
            print("Error on_data:%s" %str(e))
    
    def on_error(self, status):
        if status == 420:
            #Returning False on_data method in case rate limit occurse.
            return False
        print(status)