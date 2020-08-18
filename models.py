"""SQLAlchemy models andutility functions for twitoffs"""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twitter usres corresponding to tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15),nullable=False)

    def __repr__(self):
        return '-User{}'.format(self.name)
        