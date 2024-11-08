import oci
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from storage import object_storage_client, namespace, bucket_name   


app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app) # inicializa a extensão, configurando o ORM (Object-Relational Mapping) pra ele interagir com o db
bcrypt = Bcrypt(app) # é usado pra hash e verificação de senhas  

from routes import routes_bp
app.register_blueprint(routes_bp)

login_manager = LoginManager(app) # inicializa essa extensão, que ajuda a associar users logados com sessões
login_manager.login_view = 'routes.login' # se o user não estiver autenticado e tentar acessar uma página protegida
                                            # vai redirecionar ele pra 'routes.login', a pág de login

from models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
