from flask import Blueprint

items  = Blueprint('items',__name__)

from . import  views

"""Importe para criarção da Blueprint da aplicação"""