import os
from werkzeug.utils import secure_filename
from app import app, db
from models import User

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_profile_picture_upload(file, username, user_id):
    if not file:
        return {"success": False, "message": "Nenhuma imagem selecionada"}
    
    if file.filename == '':
        return {"success": False, "message": "Arquivo inválido"}

    if not allowed_file(file.filename):
        return {"success": False, "message": "Apenas arquivos JPG e PNG são suportados"}

    # Verifica o tamanho do arquivo
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    if file_length > app.config['MAX_CONTENT_LENGTH']:
        return {"success": False, "message": "O arquivo é muito grande. O tamanho máximo é 2MB."}
    file.seek(0)  # Reseta o ponteiro para leitura

    # Salva o arquivo
    filename = save_profile_picture(file, username, user_id)
    if filename:
        profile_picture_url = f'static/uploads/profile_pics/{filename}'
        return {"success": True, "url": profile_picture_url}
    else:
        return {"success": False, "message": "Erro ao salvar a imagem."}

def save_profile_picture(file, username, user_id):
    extension = file.filename.rsplit('.', 1)[1].lower()
    filename = f"profile_picture_{username}.{extension}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    file.save(file_path)
    user = User.query.get(user_id)
    user.profile_picture = filename
    if user:
        db.session.commit() 
    return filename

def delete_profile_picture(user):
    # Verifica se o usuário tem uma imagem de perfil personalizada
    if user.profile_picture:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], user.profile_picture)
        if os.path.exists(file_path):
            os.remove(file_path)  # Remove o arquivo do sistema

        # Atualiza o perfil do usuário para usar a imagem padrão
        user.profile_picture = None
        db.session.commit()

        # Atualiza a sessão para redefinir a imagem padrão
        return {"success": True, "message": "Foto de perfil excluída com sucesso", "default_url": 'static/images/default_profile.png'}
    else:
        return {"success": False, "message": "Nenhuma foto de perfil para excluir"}