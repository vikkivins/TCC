import oci
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config


app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app) # inicializa a extensão, configurando o ORM (Object-Relational Mapping) pra ele interagir com o db
bcrypt = Bcrypt(app) # é usado pra hash e verificação de senhas  

from routes import routes_bp
app.register_blueprint(routes_bp)

# Configurar o cliente Oracle Cloud Object Storage
config = oci.config.from_file("~/.oci/config")  # Carrega as credenciais da Oracle Cloud
object_storage_client = oci.object_storage.ObjectStorageClient(config)
namespace = object_storage_client.get_namespace().data  # Namespace único da sua conta Oracle
bucket_name = "sparkle-images"  # Nome do bucket criado

login_manager = LoginManager(app) # inicializa essa extensão, que ajuda a associar users logados com sessões
login_manager.login_view = 'routes.login' # se o user não estiver autenticado e tentar acessar uma página protegida
                                            # vai redirecionar ele pra 'routes.login', a pág de login

from models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
