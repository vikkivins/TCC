import os # permite que o flask interaja com o sistema operacional de forma segura
          # nesse caso, se certifica de que a chave secreta, por exemplo, está segura 

class Config:
    # Chave secreta para segurança do Flask
    os.environ.get('SECRET_KEY')

    # Configuração do SQLAlchemy para MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('mysql+pymysql://root@localhost/mydatabase')

    # Evita avisos desnecessários do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
