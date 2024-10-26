from flask import request, jsonify, Blueprint
from api.models import Books
from api import session

library = Blueprint('books', __name__)


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
            'publication_date': book.publication_date,
            'availability_status': book.availability_status,
            'edition': book.edition,
            'summary': book.summary
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


@library.route('/books', methods=['GET'])
def get_all_books():
    """
    Retrieve all books in the database.

    Returns:
        tuple: A JSON response of all books and the HTTP status code.
    """
    books = session.query(Books).all()
    return format_response(
        data=books,
        status='success',
        message='Tasks retrieved successfully',
        code=200
        )


@library.route('/books/<int:book_id>', methods=['GET'])
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
            code=404
            error={'details': f'No tasks were found for the given id({book_id})'}
            )
    return format_response(
        data=[book],
        status='success',
        message='Tasks retrieved successfully',
        code=200
        )
