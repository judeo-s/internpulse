import unittest
from api.models import Products
from api import session

class TestDatabase(unittest.TestCase):

    def test_products_table(self):
        # Test if the Products table is created successfully
        new_product = Products(name="Test Product")
        session.add(new_product)
        session.commit()
        
        product = session.query(Products).filter(Products.name == "Test Product").first()
        self.assertIsNotNone(product)
        self.assertIsInstance(product.id, int)
        self.assertIsInstance(product.name, str)
        self.assertEqual(product.name, "Test Product")
