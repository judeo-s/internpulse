from flask import request, jsonify, Blueprint
from api.models import Books
from api import session
from datetime import datetime
"""
This module contains all the routes for the API.

The routes are all prefixed with '/books'.

The routes are as follows:

- GET /books: Retrieve all books in the database.
- GET /books/<id>: Retrieve a specific book by ID.
- POST /books: Create a new book.
- PUT /books/<id>: Update a specific book by ID.
- DELETE /books/<id>: Delete a specific book by ID.

"""


library = Blueprint('books', __name__)


def validate_book_data(data):
    """
    Validate that the JSON data contains all the necessary keys.

    Args:
        data (dict): The JSON data from the POST request.

    Returns:
        list: A list of missing keys if the data does not validate, otherwise an empty list.
    """
    required_keys = [
        'title',
        'author',
        'genre',
        'description',
        'publication_date',
        'availability_status',
        'edition',
        'summary'
    ]
    missing_keys = [key for key in required_keys if key not in data.keys()]
    return missing_keys


def format_books_list(books_list: list):
    """
    Format a list of Books objects into a list of dictionaries that can be directly
    converted to JSON.

    Args:
        books_list (list): A list of Books objects.

    Returns:
        list: A list of dictionaries.
    """
    formatted_books = []
    for book in books_list:
        formatted_books.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'description': book.description,
            'publication_date': book.publication_date,
            'availability_status': book.availability_status,
            'edition': book.edition,
            'summary': book.summary,
            'created_at': book.created_at,
            'updated_at': book.updated_at
        })
    return formatted_books


def format_response(data=None, status='success', message='', code=200, error=None):
    """
    Format a response into a JSON response.

    Args:
        data (dict or list): The data to be returned.
        status (str): The status of the response.
        message (str): An optional message for the response.
        code (int): The HTTP status code to return.
        error (dict): An optional error dictionary.

    Returns:
        tuple: A JSON response of the formatted data and the HTTP status code.
    """
    response = {
        'status': status,
        'message': message,
        'http_code': code
    }
    if data is not None:
        response['data'] = {'tasks': format_books_list(data)}
    if error is not None:
        response['error'] = error
    return jsonify(response), code


@library.route('/books', methods=['GET'], strict_slashes=False)
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
            message='Tasks retrieved successfully',
            code=200
            )


@library.route('/books/<int:book_id>', methods=['GET'], strict_slashes=False)
def get_book(book_id):
    """
    Retrieve information about a certain book using its id.

    Args:
        book_id (int): The id of the book to retrieve.

    Returns:
        tuple: A JSON response of all books and the HTTP status code.
    """
    book = session.query(Books).filter_by(id=book_id).first()
    if book is None:
        return format_response(
            status='error',
            message='Tasks not found',
            code=404,
            error={'details': f'No tasks were found for the given id({book_id})'}
            )
    return format_response(
        data=[book],
        status='success',
        message='Tasks retrieved successfully',
        code=200
        )


@library.route('/books', methods=['POST'], strict_slashes=False)
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
                message='Task added successfully',
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