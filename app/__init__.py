from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode
from flask_uploads.flask_uploads import UploadSet, configure_uploads
from config  import config
from flask_login import LoginManager
from flask_babel import Babel
from flask_uploads import IMAGES


db = SQLAlchemy()
qr = QRcode()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
babel = Babel()
photos = UploadSet('photos', IMAGES)


def create_app(config_name):
    """Criando Aplicação com modelo factory e carregando as blueprints"""
    app = Flask(__name__) #Intanciando o app
    app.config.from_object(config[config_name])#Carregando configuração
    config[config_name].init_app(app) #iniciando app conforme a configuração
    configure_uploads(app, (photos))#Configurando uploads para a aplicação

    db.init_app(app) #iniciando Banco de dados
    login_manager.init_app(app) #iniciando o Flask-login
    babel.init_app(app) # Iniciando o Babel
    qr.init_app(app) # Inicando a Geração de QR code

    # Carregando as Blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .categories import categories as categories_blueprint
    app.register_blueprint(categories_blueprint)

    from .items import items as items_blueprint
    app.register_blueprint(items_blueprint)


    return app

