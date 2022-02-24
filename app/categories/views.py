from flask import render_template, flash, redirect, url_for
from . import categories
from .forms import CategorieForm
from app.models.models import Categorie
from .. import db
from flask_login import login_required
from random import randint


@categories.route('/nova_categoria',  methods=['GET', 'POST'])
@login_required
def new_categorie():
    """Rota para Cadastro de  nova categoria"""
    form = CategorieForm()
    if form.validate_on_submit():
        """ Adiciona os dados para ser feito o insert no banco de dados, após adicionar no banco de dados,
            retorna a mensagem padrão e em seguida recarrega a página de cadastro"""
        categorie = Categorie(name=form.name.data, photo=form.photo.data)
        db.session.add(categorie)
        db.session.commit()
        flash('Categoria Cadastrada')
        return redirect(url_for('categories.new_categorie'))
    return render_template('categories/new_categorie.html', form=form, randint=randint)

@categories.route('/consultar_categorias')
@login_required
def consult_categories():
    """Rota para puxar todas as Categorias cadastradas"""
    categories = Categorie.query.all()
    return render_template('categories/consult_categories.html', categories=categories, randint=randint)

@categories.route('/editar_categoria/<int:id>',  methods=['GET', 'POST'])
@login_required
def edit_categorie(id):
    """Função para Editar alguma categoria """
    categorie = Categorie.query.filter_by(id=id).first() # Faz a Query buscando a cátegoria pelo ID
    #dicinario para carregar os dados no form, carrega o campo com a informação da query.
    data = {
        'name': categorie.name,
        'photo': categorie.photo
    }
    # Carrega o fommúlario já passando os dados em formato de dicionário
    form = CategorieForm(data=data)
    if form.validate_on_submit():
        """Se o form vor validado adiciona as novas informações no banco de dados"""
        categorie.name = form.name.data
        categorie.photo = form.photo.data
        db.session.commit()
        flash('Categoria Atualizada')
        return redirect(url_for('categories.consult_categories'))
    return render_template('categories/edit_categorie.html', form=form, randint=randint)

@categories.route('/delete_categorie/<int:id>',  methods=['GET', 'POST'])
@login_required
def delete_categorie(id):
    """Rota Para Deletar uma categoria, faz a query com base no id e em seguida Deleta ela do banco de dados"""
    categorie = Categorie.query.filter_by(id=id).first()
    db.session.delete(categorie)
    db.session.commit()
    flash('Categoria Deletada')
    return redirect(url_for('categories.consult_categories'))