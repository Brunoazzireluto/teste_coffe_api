from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import InputRequired, Optional


class RequestForm(FlaskForm):
    """Form para Adicionar a quantidade e observações de cada item"""
    observations = TextAreaField('Informações Adicionais', validators=[Optional()])
    quantity = IntegerField(validators=[InputRequired()])

class NoteForm(FlaskForm):
    sale = SelectField('Comprador Presente?', validators=[InputRequired()], choices=[(1, 'Operação Presencial'), (4, 'Entrega a Domicilio')])
    #Como verificar a bandeira do cartão