from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, TextAreaField, FloatField, FileField
from wtforms.validators import InputRequired, DataRequired, Length
from ..models.models import Categorie
from wtforms.ext.sqlalchemy.fields import QuerySelectField

def search_categorie():
    """Função que retorna as categorias ordenadas pelo nome
        utliziada no campo de QuerySelectField.
    """
    return Categorie.query.order_by(Categorie.name)


class PlateForm(FlaskForm):
    """Formulario para Cadastrar novo Prato(item do Menu)"""
    categorie = QuerySelectField('Selecionar Categoria', query_factory=search_categorie, allow_blank=True, 
    get_label='name', validators=[InputRequired()])
    name = StringField('Nome do Prato', validators=[InputRequired(), Length(1, 40)])
    description = TextAreaField('Descrição', validators=[InputRequired()])
    price = FloatField('Preço', validators=[InputRequired()])
    photo = FileField('Enviar Foto', validators=[DataRequired()])