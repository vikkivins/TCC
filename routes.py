# routes.py

from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import db, bcrypt
from models import User, Book, Chapter, Idea
from services import handle_profile_picture_upload, delete_profile_picture

routes_bp = Blueprint('routes', __name__)

# Upload de imagens
@routes_bp.route('/upload', methods=['POST'])
def upload_profile_picture():
    result = handle_profile_picture_upload(request.files.get('profile_picture'), session.get('username'), user_id = current_user.user_id)
    #return jsonify(result), (200 if result['success'] else 400)
    return redirect(url_for('routes.profile'))

@routes_bp.route('/profile', methods=['GET'])
def profile():
    # Obter o usuário logado
    user_id = current_user.user_id
    user = User.query.get(user_id)

    # Caminho da imagem de perfil
    profile_picture_url = session.get('profile_picture_url') or 'uploads/profile_pics/default_profile.png'
    if 'profile_picture_url' not in session or user.profile_picture is None or profile_picture_url is not user.profile_picture:
        profile_picture_url = f'uploads/profile_pics/{user.profile_picture if user.profile_picture else "default_profile.png"}'
        session['profile_picture_url'] = profile_picture_url

    # Capturar mensagens de erro ou sucesso do upload
    upload_error = request.args.get('upload_error')
    upload_success = request.args.get('upload_success')

    # Obter os livros e o total de dias escrevendo
    books = user.books  # Lista de livros associados ao usuário
    quantidade_dias = user.writing_streak if hasattr(user, 'writing_streak') else 0  # Exemplo para "dias escrevendo"

    return render_template(
        'profile.html',
        user=user,
        profile_picture=profile_picture_url,
        upload_error=upload_error,
        upload_success=upload_success,
        book=books,
        quantidade=quantidade_dias
    )

@routes_bp.route('/delete_profile_picture', methods=['POST'])
def delete_profile_picture_route():
    user = User.query.get(current_user.user_id)
    result = delete_profile_picture(user)

    if result["success"]:
        session['profile_picture_url'] = result["default_url"]
        return redirect(url_for('routes.profile', upload_success=result["message"]))
    else:
        return redirect(url_for('routes.profile', upload_error=result["message"]))


@routes_bp.route('/register.html', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Verifica se o email já está cadastrado
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Este e-mail já está cadastrado. Por favor, use outro e-mail.', 'danger')
            return render_template('register.html', email=email, name=name, username=username, email_error=True)
        
        # Criação do novo usuário
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email=email, username=username, name=name, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Sua conta foi criada com sucesso! Você já pode fazer login.', 'success')
        return redirect(url_for('routes.login'))
    
    return render_template('register.html')


@routes_bp.route('/login.html', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=request.form.get('remember'))
            session['username'] = user.username  # Save the username in session
            return redirect(url_for('routes.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@routes_bp.route('/logout', methods=['POST']) 
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('routes.login'))

@routes_bp.route('/forgot.html', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        # colocar redefinicao de senha aq
        flash('If an account with that email exists, you will receive a password reset email shortly.', 'info')
        return redirect(url_for('routes.login'))
    return render_template('forgot.html')

@routes_bp.route('/')
@login_required
def home():
    books = Book.query.filter_by(user_id=current_user.user_id).all()
    ideas = Idea.query.filter_by(user_id=current_user.user_id).all()
    return render_template('home.html', books=books, ideas=ideas)

@routes_bp.route('/create_book', methods=['GET', 'POST'])
@login_required
def create_book():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        # Criação do novo livro com user_id
        new_book = Book(name=name, description=description, user_id=current_user.user_id)
        db.session.add(new_book)
        db.session.commit()
        flash('Livro criado com sucesso!', 'success')
        return redirect(url_for('routes.home'))

    return render_template('create_book.html')


@routes_bp.route('/books')
@login_required
def list_books():
    books = Book.query.filter_by(user_id=current_user.user_id).all()
    return render_template('list_books.html', books=books)

@routes_bp.route('/book/<int:book_id>')
@login_required
def view_book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('view_book.html', book=book)

@routes_bp.route('/book/<int:book_id>/add_chapter', methods=['POST'])
@login_required
def add_chapter(book_id):
    book = Book.query.get_or_404(book_id)
    title = request.form.get('title')
    content = request.form.get('content')
    new_chapter = Chapter(title=title, content=content, book_id=book.book_id)
    db.session.add(new_chapter)
    db.session.commit()
    flash('Capítulo adicionado com sucesso!', 'success')
    return redirect(url_for('routes.view_book', book_id=book.book_id))

# CRUD dos capítulos

@routes_bp.route('/chapter/<int:chapter_id>/delete', methods=['POST'])
@login_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    book = Book.query.get(chapter.book_id)
    
    if book.user_id != current_user.user_id:
        flash('Você não tem permissão para excluir este capítulo.', 'danger')
        return redirect(url_for('routes.view_book', book_id=book.book_id))
    
    db.session.delete(chapter)
    db.session.commit()
    flash('Capítulo excluído com sucesso!', 'success')
    return redirect(url_for('routes.view_book', book_id=book.book_id))

# CRUD dos livros

@routes_bp.route('/book/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.user_id != current_user.user_id:
        flash('Você não tem permissão para editar este livro.', 'danger')
        return redirect(url_for('routes.home'))
    
    if request.method == 'POST':
        book.name = request.form.get('name')
        book.description = request.form.get('description')
        db.session.commit()
        flash('Livro atualizado com sucesso!', 'success')
        return redirect(url_for('routes.view_book', book_id=book.book_id))
    
    return render_template('edit_book.html', book=book)

@routes_bp.route('/book/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.user_id != current_user.user_id:
        flash('Você não tem permissão para excluir este livro.', 'danger')
        return redirect(url_for('routes.home'))
    
    # Delete all chapters associated with the book
    Chapter.query.filter_by(book_id=book.book_id).delete()
    
    db.session.delete(book)
    db.session.commit()
    flash('Livro e seus capítulos foram excluídos com sucesso!', 'success')
    return redirect(url_for('routes.home'))

# IDEIAS CRUD

@routes_bp.route('/create_idea', methods=['GET', 'POST'])
@login_required
def create_idea():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        new_idea = Idea(title=title, content=content, user_id=current_user.user_id)
        db.session.add(new_idea)
        db.session.commit()
        flash('Ideia criada com sucesso!', 'success')
        return redirect(url_for('routes.home'))

    return render_template('create_idea.html')

@routes_bp.route('/idea/<int:idea_id>')
@login_required
def view_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    return render_template('view_idea.html', idea=idea)

@routes_bp.route('/idea/<int:idea_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    if idea.user_id != current_user.user_id:
        flash('Você não tem permissão para editar esta ideia.', 'danger')
        return redirect(url_for('routes.home'))
    
    if request.method == 'POST':
        idea.title = request.form.get('title')
        idea.content = request.form.get('content')
        db.session.commit()
        flash('Ideia atualizada com sucesso!', 'success')
        return redirect(url_for('routes.view_idea', idea_id=idea.idea_id))
    
    return render_template('edit_idea.html', idea=idea)

@routes_bp.route('/idea/<int:idea_id>/delete', methods=['POST'])
@login_required
def delete_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    if idea.user_id != current_user.user_id:
        flash('Você não tem permissão para excluir esta ideia.', 'danger')
        return redirect(url_for('routes.home'))
    
    db.session.delete(idea)
    db.session.commit()
    flash('Ideia excluída com sucesso!', 'success')
    return redirect(url_for('routes.home'))