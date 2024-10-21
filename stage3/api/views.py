from api import app, session
from flask import request, jsonify, Blueprint
from sqlalchemy.exc import NoResultFound
from api.models import Products
"""
A module to handle all http requests to the Flask application
"""


root = Blueprint('root', __name__)

@root.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form.get('name').lower()
        if product_name:
            new_product = Products(name=product_name)
            session.add(new_product)
            session.commit()
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': 'invalid request'}), 400

    if request.method == 'GET':
        query = request.args.get("name")
        if query:
            products = session.query(Products).filter(Products.name == query)
        else:
            products = session.query(Products).all()

        product_list = [{'id': product.id, 'name': product.name} for product in products]
        return jsonify({'status': 'success', 'products': product_list})


@root.route("/id/<ID>", methods=['GET'])
def name_by_id(ID):
    product = None
    if ID:
        try:
            product = session.query(Products).filter(Products.id == ID).one()
        except NoResultFound as error:
            return {'status': 'error', "msg": f"id [{ID}] does not exist"}

    product = {'id': product.id, 'name': product.name}
    return jsonify({'status': 'success', 'product': product})
