from api import app, session
from flask import request, jsonify, Blueprint
from sqlalchemy.exc import NoResultFound
from api.models import Products
"""
A module to handle all http requests to the Flask application
"""


root = Blueprint('root', __name__)


@root.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    body_name = request.form.get('name')
    query_name = request.args.get("name")

    """Handling POST requests"""
    if request.method == 'POST':
        existing_product = None
        if body_name:
            try:
                existing_product = session.query(
                        Products).filter(
                                Products.name == body_name.lower()).one()
                return jsonify(
                        {'status': 'error', 'message': 'product already exists'}), 409
            except NoResultFound as error:
                new_product = Products(name=body_name)
                session.add(new_product)
                session.commit()
                return jsonify({'status': 'success',
                    'message': 'product has been added'}), 201
        return jsonify({'status': 'error', 'message': 'invalid request'}), 400

    """Handling GET requests"""
    if request.method == 'GET':
        if query_name:
            try:
                product = session.query(Products).filter(
                        Products.name == query_name.lower()).one()
                product = {'id': product.id, 'name': product.name}
                return jsonify({'status': 'success', 'product': product}), 200
            except NoResultFound as error:
                return jsonify({'status': 'error',
                    'message': f'product [{query_name}] does not exist'}), 404
        else:
            products = session.query(Products).all()
        product_list = [{'id': product.id, 'name': product.name} for product in products]
        return jsonify({'status': 'success', 'products': product_list}), 200

    """Handling PUT requests"""
    if request.method == 'PUT':
        query_product = None
        body_product = None
        if query_name and body_name:
            try:
                query_product = session.query(Products).filter(
                    Products.name == query_name.lower()).one()
            except NoResultFound as error:
                return jsonify({'status': 'error',
                    'message': f'product [ {query_name} ] does not exist'}), 404
            try:
                body_product = session.query(Products).filter(
                    Products.name == body_name.lower()).one()
                return jsonify({'status': 'error',
                    'message': f'product [ {body_name} ] already exists'}), 409
            except NoResultFound as error:
                query_product.name = body_name.lower()
                session.commit()
                return jsonify({'status': 'success',
                    'message': 'product has been updated'}), 200
        return jsonify({'status': 'error', 'message': 'invalid request'}), 400

    """Handling DELETE request"""
    if request.method == 'DELETE':
        if query_name:
            try:
                product = session.query(Products).filter(
                        Products.name == query_name.lower()).one()
                session.delete(product)
                return jsonify({'status': 'success',
                    'message': f'product has been deleted'}), 200
            except NoResultFound as error:
                return jsonify({'status': 'error',
                    'message': f'product [ {query_name} ] does not exist'}), 404
        return jsonify({'status': 'error', 'message': 'invalid request'}), 400


@root.route("/id/<ID>", methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def product_by_id(ID):
    query_name = request.args.get("name")
    body_name = request.form.get("name")
    product = None
    if ID:
        try:
            product = session.query(Products).filter(Products.id == ID).one()
        except NoResultFound as error:
            return jsonify({'status': 'error',
                "message": f"id [ {ID} ] does not exist"}), 404

    if request.method == 'GET':
        product = {'id': product.id, 'name': product.name}
        return jsonify({'status': 'success', 'product': product})

    if request.method == 'PUT':
        if body_name:
            if product.name != body_name:
                product.name = body_name.lower()
                session.commit()
                return jsonify({'status': 'success',
                    'message': 'product has been updated'}), 200
            return jsonify({'status': 'error',
                'message': f'product [ {body_name} ] already exists'}), 409 
        return jsonify({'status': 'error', 'message': 'invalid request'}), 400

    if request.method == 'DELETE':
        session.delete(product)
        return jsonify({'status': 'success',
            'message': f'product has been deleted'}), 200
