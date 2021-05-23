"""Prediction of Users based on Tweet embeddings."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet
from sklearn.metrics import accuracy_score

def predict_user(user1_name, user2_name, tweet_text):
    """
    Determine and return which user is more likely to say a given Tweet.
    Example run: predict_user('austen', 'elonmusk', 'Lambda School rocks!')
    Returns 1 (corresponding to first user passed in) or 0 (second).
    """
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.ones(len(user1.tweets)),
                             np.zeros(len(user2.tweets))])
    log_reg = LogisticRegression().fit(embeddings, labels)
    # We've done our data science! Now to predict
    tweet_embedding = vectorize_tweet(tweet_text).reshape(1,-1)
    y_pred = log_reg.predict(tweet_embedding)
    y_pred_proba = log_reg.predict_proba(tweet_embedding)
    #ac_score = log_reg.score(embeddings,y_pred)
    return y_pred, y_pred_proba
