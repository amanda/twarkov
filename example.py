from twython import Twython, TwythonError
from twarkov import *

import os

# setup twitter api creds to scrape a timeline
# first set creds as environment variables
APP_KEY = os.getenv('APP_KEY')
APP_SECRET = os.getenv('APP_SECRET')
OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.getenv('OAUTH_TOKEN_SECRET')

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# get last 200 tweets from a user
# tweet content will be used to train the markov generator


def get_tweets(username):
    '''(str) -> list of tweets,
    fetches last 200 tweets from specified user'''
    try:
        user_timeline = twitter.get_user_timeline(
            screen_name=username, count=200, include_rts=False, exclude_replies=True)
        tweets = [user_timeline[i]['text']
                  for i in range(len(user_timeline) - 1)]
        return ' '.join(tweets).lower()
    except TwythonError as e:
        print e
        return e

# getting tweets
your_tweets = get_tweets('')  # YOUR TWITTER HANDLE HERE

# create a markov generator trained on tweets with an ngram of 1
twarkov_gen = MarkovGenerator(your_tweets, 1)

# see a tweet when you run the script
if __name__ == '__main__':
    print twarkov_gen.generate_tweet()
