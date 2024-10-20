class Config:
    # Chave secreta para segurança do Flask
    SECRET_KEY = 'sua_chave_secreta_aqui'

    # Configuração do SQLAlchemy para MySQL
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root@localhost/mydatabase"
    )

    # Evita avisos desnecessários do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
