from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class CategorieForm(FlaskForm):
    """Form de cadastro de categorias"""
    name = StringField('Nome da Categoria', validators=[InputRequired()])
    photo = StringField('Link do icone', validators=[InputRequired()])