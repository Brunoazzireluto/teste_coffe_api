from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models.models import Users
from .forms import LoginForm, ChangerPassword
from .. import db
from random import randint


#rotas de login e logout
@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm() #Carrega o Formulario de Login
    if form.validate_on_submit(): 
        user = Users.query.filter_by(username=form.username.data).first() #Faz a Query usando o nome de usuário
        if user is not None and user.verify_password(form.password.data):
            """Se o usuário não for fvazio e a senha for igual ao que tem no banco, faça o login"""
            login_user(user)
            next = request.args.get('next') #recupera o proxímo argumentos do método get
            if next is None or not next.startswith('/'):
                """Se o Next for vazio ou começar com / então defina o next como a pagina index"""
                next = url_for('main.index')
            return redirect(next)
        flash('Usuario ou Senha Inválida')
    return render_template('auth/login.html', form=form, randint=randint) #renderizando a pagina html

@auth.route('/logout')
@login_required #Verifica se o usuario está logado, se sim ele tem permissão para acessar a rota
def logout():
    """
    Rota de Logout
        Faz o logout usando o método padrão do flask-login, limpa a sessão e redireciona para a a rota de Login
    """
    logout_user()
    flash('Você foi desconectado')
    session.clear()
    return redirect(url_for('auth.login'))

@auth.route('/changer_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Rota para Alteração de senha"""
    form = ChangerPassword() #Carrega o form de alteração de senha
     #Verifica se o form foi enviado
    if form.is_submitted():
        #Verifica se o form foi Enviado e Validado
        if form.validate_on_submit():
            #se sim faz a query e verifica a senha antiga correspondem com a armazenada
            if current_user.verify_password(form.old_password.data):
                # Armazena o novo valor de senha
                current_user.password = form.password.data 
                db.session.add(current_user)
                #Adiciona no banco de dados
                db.session.commit()
                flash('Sua senha foi Atualizada')
                return redirect(url_for('main.index'))
            #Se a senha não for igual retorna uma mensagem padrão
            else:
                flash('Senha antiga Inválida.')
        #se Não for valídado retorna uma mensagem padrão
        else:
            flash('As senhas precisam ser iguais')
    return render_template("auth/change_password.html", form=form, randint=randint)

@auth.route('/novo_usuario', methods=['GET', 'POST'])
@login_required
def new_user():
    """Criação de Novo usuário"""
    form = LoginForm()
    #Verifica se o Form está válido
    if form.validate_on_submit():
        #Armazena os dados inseridos no formulário
        user = Users(username=form.username.data, password=form.password.data)
        db.session.add(user)
        #Adiciona o novo usuário
        db.session.commit()
        #Mostra a mensagem padrão no usuário
        flash('Usuario Criado com o login {} e senha {}'.format(form.username.data, form.password.data))
        redirect(url_for('main.index'))
    return render_template("auth/new_user.html", form=form, randint=randint)

@auth.route('/usuarios')
@login_required
def users():
    """Rota para Carregar os usuários"""
    users = Users.query.all() # Query que busca todos os usuários do banco de dados
    return render_template('auth/consult_users.html', users=users, randint=randint)

@auth.route('/delete_user/<int:id>')
@login_required
def delete_user(id):
    """Rota para Deletar um usuário n"""
    user = Users.query.filter_by(id=id).first() #Faz a Quiery  buscando o user com base no id
    if user.id == 1:
        """Se o for o usuário ADM bloqueia o delte e retorna para a página anterior"""
        flash('Usuário {} não pode ser deletado'.format(user.username))
        return redirect(url_for('auth.users'))
    else:
        """Se for outro User fazo delete e retorna a mensagem padrão voltando a página anterior"""
        db.session.delete(user)
        db.session.commit()
        flash('Usuário Deletado')
        return redirect(url_for('auth.users'))