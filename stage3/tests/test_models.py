import unittest
from api.models import Products
from api import session

class TestDatabase(unittest.TestCase):

    def test_products_table(self):
        '''
        Test if the Products table is created successfully
        '''
        new_product = Products(name="Test Product")
        session.add(new_product)
        session.commit()
        
        product = session.query(Products).filter(Products.name == "Test Product").first()
        self.assertIsNotNone(product)
        self.assertIsInstance(product.id, int)
        self.assertIsInstance(product.name, str)
        self.assertEqual(product.name, "Test Product")

    def test_id_autoincrement(self):
        '''
        Test if the id of the Products table is autoincrementing
        '''
        product1 = Products(name="Product 1")
        product2 = Products(name="Product 2")
        session.add(product1)
        session.add(product2)
        session.commit()
        
        self.assertEqual(product2.id, product1.id + 1)