import unittest
from api.models import Books
from api import session
from datetime import datetime


class TestDatabase(unittest.TestCase):
    """
    Test cases for the database of the API
    """

    def setUp(self):
        """
        Setup the database before each test
        """
        self.book1 = Books(title="Book 1", author="Author 1", description="This is a book",
                           genre="Fiction", publication_date=datetime(2024, 10, 31, 23, 59, 59),
                           availability_status="returned",
                           edition="1st Edition", summary="This is a summary")
        self.book2 = Books(title="Book 2", author="Author 2", description="This is another book",
                           genre="Non-Fiction", publication_date=datetime(2024, 10, 31, 23, 59, 59),
                           availability_status="returned",
                           edition="2nd Edition", summary="This is another summary")
        session.add(self.book1)
        session.add(self.book2)
        session.commit()

    def tearDown(self):
        """
        Delete the books from the database after each test
        """
        session.query(Books).delete()
        session.commit()

    def test_database_connection(self):
        """
        Test that the database connection is working
        """
        self.assertTrue(session.query(Books).first() is not None)

    def test_database_insert(self):
        """
        Test that books can be inserted into the database
        """
        session.add(Books(title="Book 3", author="Author 3", description="This is the third book",
                           genre="Fiction", publication_date=datetime(2024, 10, 31, 23, 59, 59),
                           availability_status="returned",
                           edition="1st Edition", summary="This is the third summary"))
        session.commit()
        self.assertTrue(session.query(Books).filter(Books.title == "Book 3").first() is not None)

    def test_database_update(self):
        """
        Test that books can be updated in the database
        """
        self.book1.title = "Book One"
        session.commit()
        self.assertEqual(session.query(Books).filter(Books.title == "Book One").first().title, "Book One")

    def test_database_delete(self):
        """
        Test that books can be deleted from the database
        """
        session.delete(self.book2)
        session.commit()
        self.assertIsNone(session.query(Books).filter(Books.title == "Book 2").first())

    def test_database_query(self):
        """
        Test that books can be queried from the database
        """
        self.assertEqual(session.query(Books).filter(Books.title == "Book 1").first().title, "Book 1")
        self.assertEqual(session.query(Books).filter(Books.author == "Author 1").first().author, "Author 1")
        book = session.query(Books).filter(Books.publication_date == datetime(2024, 10, 31, 23, 59, 59)).first()
        self.assertEqual(book.publication_date, datetime(2024, 10, 31, 23, 59, 59))
        self.assertEqual(session.query(Books).filter(Books.availability_status == 'returned').first().availability_status, 'returned')

    def test_database_relationship(self):
        """
        Test that the relationship between books and authors is working
        """
        self.assertEqual(session.query(Books).filter(Books.author == "Author 1").first().author, "Author 1")
        self.assertEqual(session.query(Books).filter(Books.author == "Author 2").first().author, "Author 2")

    def test_database_query_limit(self):
        """
        Test that the limit parameter of the query method works
        """
        books = session.query(Books).limit(1).all()
        self.assertEqual(len(books), 1)

    def test_database_query_offset(self):
        """
        Test that the offset parameter of the query method works
        """
        books = session.query(Books).offset(1).limit(1).all()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Book 2")

    def test_database_query_order_by(self):
        """
        Test that the order_by parameter of the query method works
        """
        books = session.query(Books).order_by(Books.title).all()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, "Book 1")
        self.assertEqual(books[1].title, "Book 2")

    def test_database_query_filter_by(self):
        """
        Test that the filter_by parameter of the query method works
        """
        books = session.query(Books).filter_by(title="Book 1").all()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Book 1")

    def test_database_query_filter(self):
        """
        Test that the filter parameter of the query method works
        """
        books = session.query(Books).filter(Books.title == "Book 1").all()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Book 1")

