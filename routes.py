# routes.py

from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import db, bcrypt, object_storage_client, namespace, bucket_name
from models import User, Book, Chapter, Idea
from services import generate_par_url

routes_bp = Blueprint('routes', __name__)


# Upload de imagens
@routes_bp.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    user_id = request.form['user_id']  # Capturar o ID do usuário

    if file:
        filename = secure_filename(file.filename)
        file_path = f"/tmp/{filename}"

        # Enviar imagem para o Oracle Cloud Object Storage
        with open(file_path, "rb") as f:
            object_storage_client.put_object(namespace, bucket_name, filename, f)

        # Gerar URL PAR para acesso temporário à imagem
        image_url = generate_par_url(filename, object_storage_client, namespace, bucket_name)

        # Atualizar o campo no banco de dados com o URL temporário
        user = User.query.get(user_id)
        user.profile_picture = image_url  # Atualiza a URL temporária da imagem
        db.session.commit()

        return "Imagem enviada com sucesso!"
    
# Verificar se a URL da imagem está na sessão
# renderiza o perfil

@routes_bp.route('/profile', methods=['GET'])
def profile():
    user_id = current_user.id
    user = User.query.get(user_id)

    # Verificar se a imagem do perfil já está na sessão
    if 'profile_picture_url' in session:
        profile_picture_url = session['profile_picture_url']
    else:
        # Se não estiver na sessão, gerar um novo URL temporário
        filename = user.profile_picture.split('/')[-1]  # Extrair o nome do arquivo do URL salvo no banco de dados
        profile_picture_url = generate_par_url(filename, object_storage_client, namespace, bucket_name)

        # Armazenar o novo URL na sessão
        session['profile_picture_url'] = profile_picture_url

    return render_template('profile.html', profile_picture=profile_picture_url)
