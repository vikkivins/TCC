from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import db, bcrypt, config, object_storage_client, namespace, bucket_name
from models import User, Book, Chapter, Idea

routes_bp = Blueprint('routes', __name__)


# Upload de imagens 

@routes_bp.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    user_id = request.form['user_id']  # Exemplo de capturar o ID do usuário
    
    if file:
        filename = secure_filename(file.filename)
        file_path = f"/tmp/{filename}"

        # Enviar imagem para o Oracle Cloud Object Storage
        with open(file_path, "rb") as f:
            object_storage_client.put_object(namespace, bucket_name, filename, f)

        # Construir URL da imagem
        image_url = f"https://objectstorage.{config['region']}.oraclecloud.com/n/{namespace}/b/{bucket_name}/o/{filename}"

        # Atualizar o campo no banco de dados
        user = User.query.get(user_id)
        user.profile_picture = image_url  # Atualiza a URL da imagem
        db.session.commit()

        return "Imagem enviada com sucesso!"
