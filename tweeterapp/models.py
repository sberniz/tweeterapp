"""SQLAlchemy models and utility functions for TwitOff."""
from flask_sqlalchemy import SQLAlchemy
DB = SQLAlchemy()
class User(DB.Model):
    """Twitter users corresponding to Tweets."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    def __repr__(self):
        return '-User {}-'.format(self.name)
class Tweet(DB.Model):
    """Tweet text and data."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))  # Allows for text + links
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
    def __repr__(self):
        return '-Tweet {}-'.format(self.text)


def insert_example_users():
    """Example data to play with."""
    austen = User(id=1, name='austen')
    elon = User(id=2, name='elonmusk')
    sanberniz = User(id=3, name='sanberniz')
    NASA = User(id=4,name='NASA')
    DB.session.add(austen)
    #austentweet = Tweet(id=1,text="This is LambdaSchool")
    #austen.tweets.append(austentweet)
    DB.session.add(elon)
    #Inserting two more users part of Assignment
    DB.session.add(sanberniz)
    DB.session.add(NASA)
    DB.session.commit()

def insert_example_tweet():
    austentweet = Tweet(id=1,text="This is LambdaSchool",user_id=1)
    elontweet = Tweet(id=2,text="SpaceX is the best",user_id=2)
    elontweet2 = Tweet(id=5,text="New Tesla Truck Soon",user_id=2)
    elontweet3 = Tweet(id=6,text="Tesla Model S best performance",user_id=2)
    nasatweet = Tweet(id=3,text="Space Shuttle History",user_id=4)
    sberniztweet = Tweet(id=4,text="Lambda School Data Science Student",user_id=3)

    DB.session.add(austentweet)
    DB.session.add(elontweet)
    DB.session.add(elontweet2)
    DB.session.add(elontweet3)
    DB.session.add(nasatweet)
    DB.session.add(sberniztweet)
    DB.session.commit()