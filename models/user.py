import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = "users"
    
    # what columns we want the table to contain:
    id = db.Column(db.Integer, primary_key=True)  # automatically generated id. Can use a UUID if you want
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    # we don't have to specify an _id, it SQLAlchemy does it for us
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        # cls.query by itself here returns: SELECT * from users
        return cls.query.filter_by(username=username).first() # only take the first row

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()