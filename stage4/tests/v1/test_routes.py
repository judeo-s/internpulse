import unittest
import json
from api.v1.models import Books
from datetime import datetime
from api import session, app


version = '/api/v1'


class TestRoutes(unittest.TestCase):
    """
    Test cases for the API routes
    """

    def setUp(self):
        """
        Setup the test client and add some books to the database
        """
        self.book1 = Books(title="Book 1", author="Author 1", genre="Non-Fiction",
                           publication_date=datetime(2024, 10, 31, 23, 59, 59).date().isoformat(),
                           availability_status="available", edition="1st Edition",
                           summary="This is the first book", description="This is the first book")
        self.book2 = Books(title="Book 2", author="Author 2", genre="Fiction",
                           publication_date=datetime(2024, 10, 31, 23, 59, 59).date().isoformat(),
                           availability_status="returned", edition="1st Edition",
                           summary="This is the second book", description="This is the second book")
        self.book3 = Books(title="Book 3", author="Author 3", genre="Non-Fiction",
                           publication_date=datetime(2024, 10, 31, 23, 59, 59).date().isoformat(),
                           availability_status="available", edition="1st Edition",
                           summary="This is the third book", description="This is the third book")
        session.add_all([self.book1, self.book2, self.book3])
        self.client = app.test_client()
        session.commit()

    def tearDown(self):
        """
        Delete the books from the database after each test
        """
        session.query(Books).delete()
        session.commit()

    def test_get_all_books(self):
        """
        Test that a GET request to '/books' returns a list of all books in the database
        """
        response = self.client.get(f'{version}/books')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['data']['books']), 3)

    def test_get_book_by_id(self):
        """
        Test that a GET request to '/books/<id>' returns a book with the given id
        """
        response = self.client.get(f'{version}/books/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['data']['books'][0]['title'], 'Book 1')
        self.assertEqual(data['data']['books'][0]['author'], 'Author 1')

    def test_get_book_by_id_non_existent(self):
        """
        Test that a GET request to '/books/<id>' with a non-existent id returns a 404 status code
        """
        response = self.client.get(f'{version}/books/0')
        self.assertEqual(response.status_code, 404)

    def test_post_book(self):
        """
        Test that a POST request to '/books' creates a new book
        """
        data = {'title': 'Book 4', 'author': 'Author 4',
                'genre': 'Fiction', 'publication_date': '2024-10-31',
                'availability_status': 'returned', 'edition': '1st Edition',
                'summary': 'This is the fourth book', 'description': 'This is the fourth book'}
        response = self.client.post(f'{version}/books', data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['data']['books'][0]['title'], 'Book 4')
        self.assertEqual(data['data']['books'][0]['author'], 'Author 4')

    def test_post_book_missing_title(self):
        """
        Test that a POST request to '/books' with missing title returns a 400 status code
        """
        data = {'author': 'Author 4',
                'genre': 'Fiction', 'publication_date': '2024-10-31',
                'availability_status': 'returned', 'edition': '1st Edition',
                'summary': 'This is the fourth book', 'description': 'This is the fourth book'}
        response = self.client.post(f'{version}/books', data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_book_missing_author(self):
        """
        Test that a POST request to '/books' with missing author returns a 400 status code
        """
        data = {'title': 'Book 4',
                'genre': 'Fiction', 'publication_date': '2024-10-31',
                'availability_status': 'returned', 'edition': '1st Edition',
                'summary': 'This is the fourth book', 'description': 'This is the fourth book'}
        response = self.client.post(f'{version}/books', data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_book_missing_publication_date(self):
        """
        Test that a POST request to '/books' with missing publication date returns a 400 status code
        """
        data = {'title': 'Book 4', 'author': 'Author 4',
                'genre': 'Fiction',
                'availability_status': 'returned', 'edition': '1st Edition',
                'summary': 'This is the fourth book', 'description': 'This is the fourth book'}
        response = self.client.post(f'{version}/books', data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_book_missing_genre(self):
        """
        Test that a POST request to '/books' with missing genre returns a 400 status code
        """
        data = {'title': 'Book 4', 'author': 'Author 4',
                'publication_date': '2024-10-31',
                'availability_status': 'returned', 'edition': '1st Edition',
                'summary': 'This is the fourth book', 'description': 'This is the fourth book'}
        response = self.client.post(f'{version}/books', data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_book_update(self):
        """
        Test that a PUT request to '/books/<id>' updates a book with the given id
        """
        data = {'title': 'Book 1', 'author': 'Author 1',
                'genre': 'Non-Fiction', 'publication_date': '2024-10-31',
                'availability_status': 'returned', 'edition': '1st Edition',
                'summary': 'This is the first updated book', 'description': 'This is the first updated book'}
        response = self.client.put(f'{version}/books/1', data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['data']['books'][0]['title'], 'Book 1')
        self.assertEqual(json.loads(response.data)['data']['books'][0]['author'], 'Author 1')
        self.assertEqual(json.loads(response.data)['data']['books'][0]['genre'], 'Non-Fiction')

    def test_put_book_update_non_existent(self):
        """
        Test that a PUT request to '/books/<id>' with a non-existent id returns a 404 status code
        """
        data = {'title': 'Book 4', 'author': 'Author 4',
                'genre': 'Fiction', 'publication_date': '2024-10-31',
                'availability_status': 'returned', 'edition': '1st Edition',
                'summary': 'This is the fourth book', 'description': 'This is the fourth book'}
        response = self.client.put(f'{version}/books/0', data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_put_book_update_missing_title(self):
        """
        Test that a PUT request to '/books/<id>' with missing title returns a 400 status code
        """
        data = {'author': 'Author 4',
                'genre': 'Fiction', 'publication_date': '2024-10-31',
                'availability_status': 'returned', 'edition': '1st Edition',
                'summary': 'This is the fourth book', 'description': 'This is the fourth book'}
        response = self.client.put(f'{version}/books/1', data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_book_update_missing_author(self):
        """
        Test that a PUT request to '/books/<id>' with missing author returns a 400 status code
        """
        data = {'title': 'Book 4',
                'genre': 'Fiction', 'publication_date': '2024-10-31',
                'availability_status': 'returned', 'edition': '1st Edition',
                'summary': 'This is the fourth book', 'description': 'This is the fourth book'}
        response = self.client.put(f'{version}/books/1', data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_book_update_missing_publication_date(self):
        """
        Test that a PUT request to '/books/<id>' with missing publication date returns a 400 status code
        """
        data = {'title': 'Book 4', 'author': 'Author 4',
                'genre': 'Fiction',
                'availability_status': 'returned', 'edition': '1st Edition',
                'summary': 'This is the fourth book', 'description': 'This is the fourth book'}
        response = self.client.put(f'{version}/books/1', data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_book_update_missing_genre(self):
        """
        Test that a PUT request to '/books/<id>' with missing genre returns a 400 status code
        """
        data = {'title': 'Book 4', 'author': 'Author 4',
                'publication_date': '2024-10-31',
                'availability_status': 'returned', 'edition': '1st Edition',
                'summary': 'This is the fourth book', 'description': 'This is the fourth book'}
        response = self.client.put(f'{version}/books/1', data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_book(self):
        """
        Test that a DELETE request to '/books/<id>' deletes a book with the given id
        """
        response = self.client.delete(f'{version}/books/1')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(session.query(Books).filter(Books.id == 1).first())

    def test_delete_book_non_existent(self):
        """
        Test that a DELETE request to '/books/<id>' with a non-existent id returns a 404 status code
        """
        response = self.client.delete(f'{version}/books/0')
        self.assertEqual(response.status_code, 404)

    def test_delete_book_invalid_id(self):
        """
        Test that a DELETE request to '/books/<id>' with an invalid id returns a 400 status code
        """
        response = self.client.delete(f'{version}/books/invalid_id')
        self.assertEqual(response.status_code, 400)
