from email.policy import default
from enum import unique
from sqlalchemy import true
from sqlalchemy.orm import backref
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .. import login_manager


# class Ncm(db.Model):
        
#     __tablename__ = 'ncms'
#     code = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(100))

#     @staticmethod
#     def add_ncm():
#         """Adiciona os ncms automaticamente no banco de dados"""
#         ncms = [
#             {'code':09011200, 'description':'Café Descafeinado'},{'code':09012100, 'description':'Café Não descafeinado'},
#             {'code':, 'description':}
#         ]




class Categorie(db.Model):
    """
    Classe para criação da tabela de Categorias
    """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    photo = db.Column(db.String(200))
    plates = db.relationship('Plate', backref='categorie_id', lazy='dynamic')
    


class  Plate(db.Model):
    """
    Classe para criação da tabela de Pratos.
    Tem ligação com a tabela de Categorias
    """
    __tablename__ = 'plates'
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    photo = db.Column(db.String(200), unique=True)
    id_categorie = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    requests = db.relationship('Request', backref='plate_id', lazy='dynamic')


class Request(db.Model):
    """
    Classe para criação da tabela de Pedidos. 
    """
    __tablename__ = 'Requests'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    id_request = db.Column(db.Integer, unique=False)
    id_plate = db.Column(db.Integer, db.ForeignKey('plates.id'), nullable=False)
    observations = db.Column(db.Text, nullable=True)
    quantity =  db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)
    
    
class RequestInfo(db.Model):
    """
    Classe para criação da tabela de Informações do Pedido.
     Adicionado Somente uma vez no banco de dados
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    id_request = db.Column(db.Integer, unique=true)
    date = db.Column(db.DateTime)
    status = db.Column(db.String(12), nullable=True, default='Aguardando') # Outras opções -Preparando - pronto - Entregue
    name = db.Column(db.String(50), nullable=True , default=id_request)
   


class Users(UserMixin, db.Model):
    """
    Classe para criação da tabela de Usuários
    """
    __tableame__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    @staticmethod
    def insert_adm():
        """
        Função que Adiciona o usuário Mestre no app
        """
        user = Users(username='ADM', password='123')
        db.session.add(user)
        db.session.commit()

    @property
    def password(self):
        """
        Função para definir erro para o campo senha
        """
        raise AttributeError('Senha não pode ser lida')

    @password.setter
    def password(self, password):
        """
        Função para pegar a senha e definir um hash de criptografia
        """
        self.password_hash  = generate_password_hash(password)

    def verify_password(self, password):
        """
        Função para verificar se a senha armazenada é igual o hash
        """
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(id):
        """
        carrega o Id do usuário atual
        """
        return Users.query.get(int(id))

    def get_id(self):
        """ Retornar o Id do usuário atual"""
        return (self.id)

class Company(db.Model):
    """Classe para criar a tabela da empresa no banco de dados """
    __tablename__ = 'company'
    cnpj = db.Column(db.String(15), primary_key=True)
    company_name = db.Column(db.String(100))
    name_fantasy = db.Column(db.String(100), nullable=True)
    adress = db.Column(db.String(200))

    @staticmethod
    def add_company():
        """Função para inserir automaticamente as informações da empresa no banco de dados"""
        company = Company(cnpj=33152305000178,company_name='Cafeteria cafe com cookies ltda',name_fantasy="Cookies N' Coffe",adress='Av Leonardo da Vinci, 1075, loja 11,  São Paulo-SP')
        db.session.add(company)
        db.session.commit()
        print('Empresa criada')