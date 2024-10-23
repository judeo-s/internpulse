import unittest
from api import app, session
from api.models import Products
import json
"""
Tests for the API views
"""

class TestViews(unittest.TestCase):
    def setUp(self):
        """
        Setup the test client and add some products to the database
        """
        self.app = app.test_client()
        self.app.post('/', data={'name': 'Test Product1'})
        self.app.post('/', data={'name': 'Test Product2'})
        self.app.post('/', data={'name': 'Test Product3'})

    def tearDown(self):
        """
        Delete all products from the database after each test
        """
        session.query(Products).delete()
        session.commit()    

    def test_get_all_no_products(self):
        """
        Test that a GET request to '/' returns a list of products
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(len(json.loads(response.data.decode('utf-8'))['products']), 3)

    def test_get_all_products_with_data(self):
        """
        Test that a GET request to '/' returns a list of products with data
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.data.decode('utf-8'))['products'][0], {"id": 1, "name": "Test Product1"}   )

    def test_post_product(self):
        """
        Test that a POST request to '/' creates a new product
        """
        response = self.app.post('/', data={'name': 'Test Product4'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.data.decode('utf-8')), {'status': 'success',
                    'message': 'product has been added'})
        self.app.delete('/id/4')

    def test_post_product_invalid_request(self):
        """
        Test that a POST request to '/' with invalid data returns a 400 status code
        """
        response = self.app.post('/', data={'foo': 'bar'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.data.decode('utf-8')), {"status": "error", "message": "invalid request"})

    def test_get_product_by_id_non_existent_product(self):
        """
        Test that a GET request to '/id/<id>' with a non-existent id returns a 404 status code
        """
        response = self.app.get('/id/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.data.decode('utf-8')), {"status": "error", "message": "id [ 1 ] does not exist"})

    def test_get_product_by_id(self):
        """
        Test that a GET request to '/id/<id>' returns a product with data
        """
        response = self.app.get('/id/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.data.decode('utf-8'))['product'], {"id": 1, "name": "Test Product1"})

    def test_get_product_by_name_non_existent_product(self):
        """
        Test that a GET request to '/?name=<name>' with a non-existent name returns a 404 status code
        """
        response = self.app.get('/?name=Test+Product4')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.data.decode('utf-8')), {"status": "error", "message": "product [Test Product4] does not exist"})

    def test_get_product_by_name(self):
        """
        Test that a GET request to '/?name=<name>' returns a product with data
        """
        response = self.app.get('/?name=Test+Product3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.data.decode('utf-8'))['product'], {"id": 3, "name": "Test Product3"})

    def test_put_product_non_existent_product(self):
        """
        Test that a PUT request to '/id/<id>' with a non-existent id returns a 404 status code
        """
        self.app.delete('/id/1')
        response = self.app.put('/id/1', data={'name': 'Updated Test Product'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.data.decode('utf-8')), {"status": "error", "message": "id [ 1 ] does not exist"})

    def test_put_product(self):
        """
        Test that a PUT request to '/id/<id>' updates a product
        """
        response = self.app.put('/id/1', data={'name': 'Updated Test Product'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.data.decode('utf-8')), {'message': 'product has been updated', 'status': 'success'})

    def test_delete_product_non_existent_product(self):
        """
        Test that a DELETE request to '/id/<id>' with a non-existent id returns a 404 status code
        """
        response = self.app.delete('/id/1')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.data.decode('utf-8')), {"status": "error", "message": "id [ 1 ] does not exist"})

    def test_delete_product(self):
        """
        Test that a DELETE request to '/id/<id>' deletes a product
        """
        response = self.app.delete('/id/1')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.data.decode('utf-8')), {"status": "success", "message": "product has been deleted"})

