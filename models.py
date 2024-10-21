# models.py

from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    profile_picture = db.Column(db.String(300), nullable=True)  # Caminho da foto de perfil
    description = db.Column(db.String(300), nullable=True)
    
class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    bookcover_image = db.Column(db.String(300), nullable=True)  # Caminho da foto de capa
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chapters = db.relationship('Chapter', backref='book', lazy=True)

class Chapter(db.Model):
    chapter_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    capcover_image = db.Column(db.String(300), nullable=True)  # Caminho da imagem personalizada do capítulo
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

class Idea(db.Model):
    idea_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    ideacover_image = db.Column(db.String(300), nullable=True)  # Caminho da imagem associada à ideia
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)