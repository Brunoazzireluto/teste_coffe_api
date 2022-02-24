from os import name
from flask import render_template, flash,  redirect, url_for, request
from flask_babel import  format_decimal
from flask_login import login_required
from .forms import PlateForm
from app.models.models import Categorie, Plate
from app import db, photos
from . import items
from ..OCI.oci import UploadOci
from ..OCI.regex import Regex
from random import randint


@items.route('/novo_prato',methods=['GET', 'POST'])
@login_required
def new_plate():
    """ Rota para Cadastro de novo Prato(item no menu)"""
    form = PlateForm()
    if form.validate_on_submit():
        #Carrega a Classe UploadOci com a foto carregada e o nome do prato
        arq = UploadOci(form.photo.data, form.name.data)
        #chama o método para fazer o upload da imagem
        photo = arq.upload_image()
        #Adiciona os dados na varivale para fazer o upload no banco de dados
        plate = Plate(name=form.name.data, description=form.description.data, price=form.price.data, photo=photo, categorie_id=form.categorie.data)
        db.session.add(plate)
        db.session.commit()
        flash('Prato adicionado com Sucesso')
        return redirect(url_for('items.new_plate'))
    return render_template('items/new_plate.html', form=form, randint=randint)

@items.route('/consultar_pratos')
@login_required
def consult_plates():
    """Rota para fazer a consulta dos pratos cadastrados"""
    #Carrega a Classe Regex criada para facilitar processos de conversão
    r = Regex()
    plates = Plate.query.order_by(Plate.id_categorie).all()
    return render_template('items/consult_plates.html', plates=plates, Categorie=Categorie, randint=randint, r=r)


@items.route('/edit_plate/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_plate(id):
    """Rota para edição do prato"""
    plate = Plate.query.filter_by(id=id).first()
    categorie = Categorie.query.filter_by(id=plate.id_categorie).first()
    data = {
        'categorie': categorie,
        'name':plate.name,
        'description':plate.description,
        'price':plate.price,
        'photo':plate.photo
    }
    form = PlateForm(data=data)
    if form.validate_on_submit():
        plate.id_categorie = form.categorie.data
        plate.name = form.name.data
        plate.description = form.description.data
        plate.price = form.price.data
    return render_template('items/edit_plate.html', form=form, randint=randint)



@items.route('/delete_plate/<int:id>')
@login_required
def delete_plate(id):
    """Rota para Deletar um prato cadastrado"""
    plate = Plate.query.filter_by(id=id).first()
    db.session.delete(plate)
    db.session.commit()
    flash('Prato Excluido')
    return redirect(url_for('items.consult_plates'))