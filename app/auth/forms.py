from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    """Formulário de Login"""
    username = StringField('Usuario', validators=[DataRequired(),  Length(1, 20)])
    password = PasswordField('Senha', validators=[DataRequired()])

class ChangerPassword(FlaskForm):
    """Formulário Para trocar a senha"""
    old_password = PasswordField('Senha Atual', validators=[DataRequired()])
    password = PasswordField('Nova Senha', validators=[DataRequired(), 
                                EqualTo('password2', message='As senhas precisam ser iguais')])
    password2 = PasswordField('Confirmar Senha',validators=[DataRequired()])