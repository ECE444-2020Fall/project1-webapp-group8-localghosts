import unittest

from app import create_app, db
from flask import current_app


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

    def testLoginPage(self):
        response = self.app.test_client().get('/auth/login')
        self.assertEqual(response.status_code, 200)

    def testGroceryListPage(self):
        response = self.app.test_client().get('/auth/signup')
        self.assertEqual(response.status_code, 200)
