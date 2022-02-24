import os 

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Chave Secreta'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = 'pt'
    UPLOADED_PHOTOS_DEST = "images"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    #Casa
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql://Azzi:Bu.62991881@localhost/Coffe_time'
    #Maeda
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql://maeda-st:Maeda123@localhost/coffe_api'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'mysql://Azzi:Bu.62991881@localhost/test'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://azzireluto:Maeda.123@10.0.1.254/coffe_aldo'

config = {
    'development' : DevelopmentConfig,
    'testing': TestingConfig,
    'Production' : ProductionConfig,

    'default' : ProductionConfig
}   