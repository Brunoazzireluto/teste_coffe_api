from flask import Blueprint

auth  = Blueprint('auth',__name__)

from . import  views

"""Importe para criarção da Blueprint da aplicação"""