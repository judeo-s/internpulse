"""
A module to handle all http requests to the Flask application

This module handles all the root routes of the API. It handles
GET, POST, PUT, DELETE requests to the root route.
"""

from api import app, session
from flask import request, jsonify, Blueprint
from sqlalchemy.exc import NoResultFound
from api.models import Products


root = Blueprint('root', __name__)


@root.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    """
    Handles GET, POST, PUT, DELETE requests to the root route.
    """
    body_name = request.form.get('name')
    query_name = request.args.get("name")

    if request.method == 'POST':
        """
        Handles POST requests to the root route.

        If the request body contains a name, it checks if the product
        already exists in the database. If it does, it returns a 409
        status code with a message indicating that the product already
        exists. If it does not, it creates a new product and returns a
        201 status code with a message indicating that the product has
        been added.
        """
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

    if request.method == 'GET':
        """
        Handles GET requests to the root route.

        If a name is provided in the query parameters, it searches for
        the product in the database. If it does not exist, it returns a
        404 status code with a message indicating that the product does
        not exist. If it does, it returns a 200 status code with the
        product details.
        """
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

    if request.method == 'PUT':
        """
        Handles PUT requests to the root route.

        If a name is provided in the query parameters and the request
        body, it checks if the product already exists in the database.
        If it does, it updates the product and returns a 200 status code
        with a message indicating that the product has been updated. If
        it does not, it returns a 404 status code with a message
        indicating that the product does not exist. If the request body
        name is different from the query parameter name, it returns a
        409 status code with a message indicating that the product
        already exists.
        """
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

    if request.method == 'DELETE':
        """
        Handles DELETE requests to the root route.

        If a name is provided in the query parameters, it searches for
        the product in the database. If it does not exist, it returns a
        404 status code with a message indicating that the product does
        not exist. If it does, it deletes the product and returns a 200
        status code with a message indicating that the product has been
        deleted.
        """
        if query_name:
            try:
                product = session.query(Products).filter(
                        Products.name == query_name.lower()).one()
                session.delete(product)
                return jsonify({'status': 'success',
                    'message': f'product has been deleted'}), 204
            except NoResultFound as error:
                return jsonify({'status': 'error',
                    'message': f'product [ {query_name} ] does not exist'}), 404
        return jsonify({'status': 'error', 'message': 'invalid request'}), 400


@root.route("/id/<ID>", methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def product_by_id(ID):
    """
    Handles GET, PUT, DELETE requests to the /id/<ID> route.

    If the request method is GET, it searches for the product with the
    given ID in the database. If it does not exist, it returns a 404
    status code with a message indicating that the product does not
    exist. If it does, it returns a 200 status code with the product
    details.

    If the request method is PUT, it checks if the product with the
    given ID exists in the database. If it does not, it returns a 404
    status code with a message indicating that the product does not
    exist. If it does, it updates the product and returns a 200 status
    code with a message indicating that the product has been updated.

    If the request method is DELETE, it searches for the product with
    the given ID in the database. If it does not exist, it returns a 404
    status code with a message indicating that the product does not
    exist. If it does, it deletes the product and returns a 200 status
    code with a message indicating that the product has been deleted.
    """
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
        return jsonify({'status': 'success', 'product': product}), 200

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
            'message': f'product has been deleted'}), 204
