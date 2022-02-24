from flask import Blueprint

main  = Blueprint('main',__name__)

from . import  views, errors

"""Importe para criarção da Blueprint da aplicação"""
