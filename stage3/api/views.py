from api import app, session
from flask import request, jsonify, Blueprint
from api.models import Products
"""
A module to handle all http requests to the Flask application
"""


root = Blueprint('root', __name__)

@root.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form.get('name')
        if product_name:
            new_product = Products(name=product_name)
            session.add(new_product)
            session.commit()
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': 'invalid request'}), 400
    if request.method == 'GET':
        products = session.query(Products).all()
        product_list = [{'id': product.id, 'name': product.name} for product in products]
        return jsonify({'status': 'success', 'products': product_list})
