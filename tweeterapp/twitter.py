"""Retrieves tweets, embeddings, and persists inthe database"""
from os import getenv
import basilica
import tweepy
from .models import DB, Tweet, User

# TODO dont have raw secrets

TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = getenv('TWITTER_API_SECRET_KEY')
BASILICA = basilica.Connection(getenv('BASILICA_KEY'))

TWITTER_USERS = ['calebhicks', 'elonmusk', 'rrherr', 'SteveMartinToGo',
                 'alyankovic', 'nasa', 'sadserver', 'jkhowland', 'austen',
                 'common_squirrel', 'KenJennings', 'conanobrien',
                 'big_ben_clock', 'IAM_SHAKESPEARE']
# TODO don't have raw secrets in the code, move to .env!
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
TWITTER = tweepy.API(TWITTER_AUTH)
def add_or_update_user(username):
    try:
            
        """Add or update a user and their Tweets, error if not a Twitter user."""
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        # Lets get the tweets - focusing on primary (not retweet/reply)
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended'
        )
        for tweet in tweets:
            embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweets = Tweet(id=tweet.id, text=tweet.full_text[:300], embedding=embedding)
            db_user.tweets.append(db_tweets)
            DB.session.add(db_tweets)
    except Exception as e:
        print("Error Processing {}: {}".format(user,e))
        raise e
    else:
        DB.session.commit()

def insert_example_users():
    """Example data to play with."""
    add_or_update_user('austen')
    add_or_update_user('elonmusk')