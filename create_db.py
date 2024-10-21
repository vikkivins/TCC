from app import app, db
from models import User, Book, Chapter, Idea

with app.app_context():
    db.create_all()

print("Banco de dados criado com sucesso!")