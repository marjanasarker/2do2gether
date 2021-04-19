from unittest import TestCase
from server import app
from model import connect_to_db, db
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
    
    # def test_login(self):
    #     """Tests the login page"""

    #     result = self.client.post('/login', 
    #                                 data={"email":"andrew.gerber@gmail.com", "password": "and123"}, 
    #                                 follow_redirects=True)
    #     self.assertIn(b'<h1>Habit Page</h1>', result.data)                            

if __name__ == "__main__":
    import unittest

    unittest.main()