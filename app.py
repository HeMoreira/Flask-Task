#para ativar venv: .\env\Scripts\activate.ps1
#para rodar o programa: python app.py
"""
OBJETIVO

Desenvolver um site em que cadastramos uma lista de compras, onde listamos
produtos com seus preços e, ao final, obtemos o preço da compra total
"""
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasktask.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, default=0)
    preco = db.Column(db.Float, default=1.0)

    def __repr__(self):
        return '<Item %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        nome_produto = request.form['nome']
        quantia_produto = request.form['quantidade']
        preco_produto = request.form['preco']
        novo_produto = Todo(nome=nome_produto, quantidade=quantia_produto, preco=preco_produto)
        try:
            db.session.add(novo_produto)
            db.session.commit()
            return redirect('/')
        except:
            return "Deu errado meu mano"
    else:
        itens = Todo.query.all()
        total = 0
        for item in itens:
            total+=item.preco*item.quantidade
        total = f"R$ {total:,.2f}"
        return render_template('index.html', itens=itens, total=total)

@app.route('/diminuir_quantidade/<int:id>')
def diminuir_quantidade(id):
    produto = Todo.query.get_or_404(id)
    try:
        if produto.quantidade > 0:
            produto.quantidade = produto.quantidade - 1
            db.session.commit()
        return redirect('/')
    except:
        return "ocorreu um erro ao tentar alterar a quantidade do produto"


@app.route('/aumentar_quantidade/<int:id>')
def aumentar_quantidade(id):
    produto = Todo.query.get_or_404(id)
    try:
        produto.quantidade = produto.quantidade + 1
        db.session.commit()
        return redirect('/')
    except:
        return "ocorreu um erro ao tentar alterar a quantidade do produto"
    
@app.route('/alterar_preco/<int:id>', methods=['POST'])
def alterar_preco(id):
    produto = Todo.query.get_or_404(id)
    novo_preco = request.form['alt_preco']
    try:
        produto.preco = novo_preco
        db.session.commit()
        return redirect('/')
    except:
        return "ocorreu um erro ao tentar alterar o preço do produto"

@app.route('/delete/<int:id>')
def delete(id):
    produto = Todo.query.get_or_404(id)
    try:
        db.session.delete(produto)
        db.session.commit()
        return redirect('/')
    except:
        return "ocorreu um erro ao tentar remover o produto"



if __name__ == "__main__":
    #with app.app_context():
    #    db.create_all()
    app.run(debug=True)