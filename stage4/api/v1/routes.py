from flask import request, Blueprint
from api.v1.models import Books
from api import session
from datetime import datetime
from api.utils import format_response, validate_book_data
"""
This module contains all the routes for the API.

The routes are all prefixed with '/api/v1/books'.

The routes are as follows:

- GET /books: Retrieve all books in the database.
- GET /books/<id>: Retrieve a specific book by ID.
- POST /books: Create a new book.
- PUT /books/<id>: Update a specific book by ID.
- DELETE /books/<id>: Delete a specific book by ID.

"""


library_v1 = Blueprint('books_v1', __name__)
version = '/api/v1'


@library_v1.route(f'{version}/books', methods=['GET'], strict_slashes=False)
def get_all_books():
    """
    Retrieve all books in the database.

    Returns:
        tuple: A JSON response of all books and the HTTP status code.
    """
    if request.method == 'GET':
        books = session.query(Books).all()
        return format_response(
            data=books,
            status='success',
            message='Books retrieved successfully',
            code=200
            )


@library_v1.route(f'{version}/books/<book_id>', methods=['GET'], strict_slashes=False)
def get_book(book_id):
    """
    Retrieve information about a certain book using its id.

    Args:
        book_id (int or str): The id of the book to retrieve.

    Returns:
        tuple: A JSON response of all books and the HTTP status code.
    """
    try:
        book_id = int(book_id)
    except ValueError:
        return format_response(
            status='error',
            message='Bad request',
            code=400,
            error={'details': 'Invalid book id'}
            )
    book = session.query(Books).filter_by(id=book_id).first()
    if book is None:
        return format_response(
            status='error',
            message='Book not found',
            code=404,
            error={'details': f'No book was found for the given id({book_id})'}
            )
    return format_response(
        data=[book],
        status='success',
        message='Books retrieved successfully',
        code=200
        )


@library_v1.route(f'{version}/books', methods=['POST'], strict_slashes=False)
def add_book():
    """
    Add a new book to the library.

    Returns:
        tuple: A JSON response of the added book and the HTTP status code.
    """
    try:
        data = request.get_json()
        missing_keys = validate_book_data(data)
        if not missing_keys:
            book = Books(
                title=data['title'],
                author=data['author'],
                genre=data['genre'],
                description=data['description'],
                publication_date=datetime.strptime(data['publication_date'], '%Y-%m-%d').date().isoformat(),
                availability_status=data['availability_status'],
                edition=data['edition'],
                summary=data['summary']
            )
            session.add(book)
            session.commit()
            return format_response(
                data=[book],
                status='success',
                message='Book added successfully',
                code=201
            )
        else:
            return format_response(
                status='error',
                message='Missing required field',
                code=400,
                error={'details': f'Missing required fields: {missing_keys}'}
            )
    except ValueError as e:
        return format_response(
            status='error',
            message='Invalid date format',
            code=400,
            error={'details': e.args[0]}
            )


@library_v1.route(f'{version}/books/<book_id>', methods=['PUT'], strict_slashes=False)
def update_book(book_id):
    """
    Update the details of a specific book.

    Returns:
        tuple: A JSON response of the updated book and the HTTP status code.
    """
    try:
        book_id = int(book_id)
    except ValueError:
        return format_response(
            status='error',
            message='Bad request',
            code=400,
            error={'details': 'Invalid book id'}
            )
    try:
        book = session.query(Books).filter_by(id=book_id).first()
        if book is None:
            return format_response(
                status='error',
                message='Book not found',
                code=404,
                error={'details': f'No book was found for the given id({book_id})'}
            )
        data = request.get_json()
        missing_keys = validate_book_data(data)
        if not missing_keys:
            book = Books(
                title=data['title'],
                author=data['author'],
                genre=data['genre'],
                description=data['description'],
                publication_date=datetime.strptime(data['publication_date'], '%Y-%m-%d').date().isoformat(),
                availability_status=data['availability_status'],
                edition=data['edition'],
                summary=data['summary']
            )
            session.add(book)
            session.commit()
            return format_response(
                data=[book],
                status='success',
                message='Book updated successfully',
                code=200
            )
        else:
            return format_response(
                status='error',
                message='Missing required field',
                code=400,
                error={'details': f'Missing required fields: {missing_keys}'}
            )

    except ValueError as e:
        return format_response(
            status='error',
            message='Invalid date format',
            code=400,
            error={'details': e.args[0]}
        )


@library_v1.route(f'{version}/books/<book_id>', methods=['DELETE'], strict_slashes=False)
def delete_book(book_id):
    """
    Delete a specific book.

    Returns:
        tuple: A JSON response indicating the result of the delete operation and the HTTP status code.
    """
    try:
        book_id = int(book_id)
    except ValueError:
        return format_response(
            status='error',
            message='Bad request',
            code=400,
            error={'details': 'Invalid book id'}
            )
    book = session.query(Books).filter_by(id=book_id).first()
    if book is None:
        return format_response(
            status='error',
            message='Book not found',
            code=404,
            error={'details': f'No book was found for the given id({book_id})'}
        )
    session.delete(book)
    session.commit()
    return format_response(
        status='success',
        message='Book deleted successfully',
        code=204
    )

