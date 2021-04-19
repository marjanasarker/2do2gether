from unittest import TestCase
from server import app
from model import connect_to_db
from flask import session


class FlaskTests(TestCase):

    def setUp(self):
        """Run this before every test"""
        
        self.client = app.test_client()
        app.config['TESTING'] = True
        
    def test_index(self):
        """Testing homepage"""

        result = self.client.get("/")
        self.assertIn(b"Welcome!", result.data)

if __name__ == "__main__":
    import unittest

    unittest.main()