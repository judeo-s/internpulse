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
        response['data'] = format_books_list(data)
    if error is not None:
        response['error'] = error
    return jsonify(response), code


