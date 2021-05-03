from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session
import os


class FlaskTests(TestCase):

    def setUp(self):
        """Run this before every test"""
        
        self.client = app.test_client()
        app.config['TESTING'] = True

        
    def test_index(self):
        """Testing homepage"""

        result = self.client.get("/")
        self.assertIn(b"Welcome!", result.data)

 
class FlaskTestsDatabase(TestCase):

    def setUp(self):
        """Run this before every test"""
        
        self.client = app.test_client()
        app.config['TESTING'] = True

        #Connected to test database
        os.system('dropdb testdb')
        os.system('createdb testdb')
        connect_to_db(app, "postgresql:///testdb")

        #Creating tables and adding sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    
    def test_login(self):
        """Testing new user login"""

        result = self.client.post('/create_account', 
                                   data={"fname":"Rodrigo", "lname":"Paste", 
                                   "email":"rodrigo.paste@gmail.com", "password":"rod123"},
                                   follow_redirects=True)
        self.assertIn(b'<h1>Sign-In</h1>', result.data)
    
    
    
                           

if __name__ == "__main__":
    import unittest

    unittest.main()