from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
from sqlalchemy.orm import backref
import random

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    bookmarks = db.relationship('Bookmark', backref="user")
    
    def __repr__(self) -> str:
        return 'User>>> {self.username}'
    

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=False)
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    
    # Constructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.short_url=self.generate_short_characters()
    
    def generate_short_characters(self):
        characters = string.digits+string.ascii_letters
        selected_chars = ''.join(random.choices(characters, k=3))
        
        link = self.query.filter_by(short_url=selected_chars).first()
        if link:
            self.generate_short_characters()
        else:
            return selected_chars
    
    def __repr__(self) -> str:
        return 'Bookmark>>> {self.url}'