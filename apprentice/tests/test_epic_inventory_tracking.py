import unittest

from app import create_app, db
from flask import current_app


class InventoryTrackingTestCase(unittest.TestCase):
    def setUp(self):
        """Setup app context and database"""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """ends session and drops database"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        # TODO: replace -- this is a dummy test
        self.assertFalse(current_app is None)
