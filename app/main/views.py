from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from .  import main
from flask_login import login_required
from ..models.models import Categorie, Plate, Request, RequestInfo
from .forms import RequestForm
from random import randint
from app import db
from ..OCI.regex import Regex
import pytz
from sqlalchemy.sql import functions

sp = pytz.timezone('America/Sao_Paulo')

def query_sum(request):
    """
    Função que Retorna um valor float que é a soma do preço de todos os valores de um pedido
    
        Faz a Query com base em um id e retorna todos os items que batem com este id
         requests = [request1, request2, request3]
        Em seguida se cria uma lista vazia, cria um for para ser ser feito o loop por cada item da requests 
        e adiciona eles na lista vazia values. por fim retorna a soma dos valores na lista.

    """
    requests = Request.query.filter_by(id_request=request).all()    
    values = []
    for request in requests:
        values.append(request.value)
    return sum(values)

@main.route('/home')
@login_required
def index():
    """Página index que contem informações dos ultimos pedidos feitos e terminados """
    r= Regex()
    infos = RequestInfo.query.order_by(RequestInfo.date.desc()).limit(10)
    return render_template('index.html', randint=randint, infos=infos, Request=Request, query_sum=query_sum,r=r)


@main.route('/novo_pedido/<int:random>')
@login_required
def new_request(random):
    """Página que carrega as categorias e mostra os itens do menu."""
    r= Regex()
    form= RequestForm()
    categories = Categorie.query.all()
    return render_template('new_request.html', form=form, categories=categories, Plate=Plate, r=r, randint=randint, random=random, Request=Request)


@main.route('/add_to_cart/<int:plate_id>/<int:random>', methods=['GET', 'POST'])
@login_required
def add_to_cart(plate_id, random):
    """Função para Adicionar os itens no banco de dados dos pedidos, adiciona um item por vez"""
    form=RequestForm()
    plate=Plate.query.filter_by(id=plate_id).first()
    if form.validate_on_submit():
        request = Request(id_request=random, plate_id=plate,observations=form.observations.data, quantity=form.quantity.data, value=(plate.price*form.quantity.data))
        db.session.add(request)
        db.session.commit()
        flash('Pedido adicionado ao carrinho')
    return redirect(url_for('main.new_request', random=random))


@main.route('/Pedido_N<int:id>')
@login_required
def cart(id):
    """Rota de carregamento dos itens adicionados no pedido"""
    r = Regex()
    requests = Request.query.filter_by(id_request=id).all()
    prices = []
    for request in requests:
        prices.append(request.value)
    final_price = sum(prices)
    return render_template('cart.html', requests=requests, id=id, Plate=Plate, randint=randint, sum=sum, r=r, final_price=final_price)


@main.route('/delete_item/<int:id_plate>/<int:id_request>')
@login_required
def delete_item(id_plate,id_request):
    """Rota de exclusão de item do banco de dados """
    item = Request.query.filter_by(id_request=id_request).filter_by(id_plate=id_plate).first()
    db.session.delete(item)
    db.session.commit()
    flash('Item Removido')
    return redirect(url_for('main.cart', id=id_request))

@main.route('/fechar_pedido/<int:id_request>')
@login_required
def close_request(id_request):
    """Rota para fechar pedido e adicionar informação no banco de dados"""
    date = datetime.today().astimezone() #Puxa a Data atual com base na timezone da Maquina
    infos = RequestInfo(id_request=id_request, date=date)
    db.session.add(infos)
    db.session.commit()
    flash('Pedido Fechado')
    return redirect(url_for('main.load'))

@main.route('/loading')
@login_required
def load():
    return render_template('load.html')




"""
Paginas do app

Cadastrar pedido
Editar pedido

adicionar/editar/remover prato

adicionar logica para combos

pediddos anterioes

ver com renato pagamentos

paginas de pagamento ->
Paginas de Notas ->

desing

fazer pedido (pratos aparecem em cards)
categorias e pratos con forms e tabelas igual o erp 
pedidos anteriores com tabela e vizualizar os pratos
primaria  #ed9121
secundaria #696969
preto #111111
branco #f5f5f5

emissão de nota com Load bonitinho
"""