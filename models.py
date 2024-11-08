# models.py

from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    profile_picture = db.Column(db.String(300), nullable=True)  # Path to profile picture
    description = db.Column(db.String(300), nullable=True)
    books = db.relationship('Book', backref='user', lazy=True)
    ideas = db.relationship('Idea', backref='user', lazy=True)

    def get_id(self):
            # Override the get_id method to use user_id instead of id
            return str(self.user_id)

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    bookcover_image = db.Column(db.String(300), nullable=True)  # Path to cover image
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    chapters = db.relationship('Chapter', backref='book', lazy=True)

class Chapter(db.Model):
    chapter_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    capcover_image = db.Column(db.String(300), nullable=True)  # Path to chapter image
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)

class Idea(db.Model):
    idea_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    ideacover_image = db.Column(db.String(300), nullable=True)  # Path to idea image
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

