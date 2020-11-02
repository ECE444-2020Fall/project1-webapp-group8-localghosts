import unittest
from flask import current_app
from app import create_app, db


class ErrorPageTestCase(unittest.TestCase): 
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test written by Ahmed Rosanally

    def testErrorPage(self):
        response = self.app.test_client().get('/blurr')
        self.assertEqual(response.status_code, 404)