import requests as http_request
from flask import make_response
from flask import Flask
from database.database import db
from flask import jsonify, request
from database.models import Pedido

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

import sys
if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    # cria o banco de dados
    with app.app_context():
        db.create_all()
    # Finaliza a execução do programa
    print("Database created successfully")
    sys.exit(0)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/novo', methods=['POST'])
def create_pedido():
    data = request.json
    pedido = Pedido(name=data["name"], email=data["email"], desc=data["desc"])
    db.session.add(pedido)
    db.session.commit()
    #RETORNAR ID AO CONFIMAR FUNCIONAMENTO
    return jsonify(pedido.serialize())

@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    pedidos = Pedido.query.all()
    return_pedidos = []
    for pedido in pedidos:
        return_pedidos.append(pedido.serialize())
    return jsonify(return_pedidos)

@app.route("/pedidos/<int:id>", methods=["GET"])
def get_pedido(id):
    pedido = Pedido.query.get(id)
    #RETORNAR ID AO CONFIMAR FUNCIONAMENTO
    return jsonify(pedido.serialize())

@app.route("/pedidos/<int:id>", methods=["PUT"])
def update_pedido(id):
    data = request.json
    pedido = Pedido.query.get(id)
    pedido.name = data["name"]
    pedido.email = data["email"]
    pedido.desc = data["desc"]
    db.session.commit()
    return jsonify(pedido.serialize())

@app.route("/pedidos/<int:id>", methods=["DELETE"])
def delete_pedido(id):
    pedido = Pedido.query.get(id)
    db.session.delete(pedido)
    db.session.commit()
    return jsonify(pedido.serialize())
