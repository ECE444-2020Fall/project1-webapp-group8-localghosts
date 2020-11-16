import unittest

from app import create_app, db
from flask import current_app


class BasicsTestCase(unittest.TestCase):
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
        """Confirms that the current application exists"""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """Ensures that configuration is set to testing"""
        self.assertTrue(current_app.config["TESTING"])


class DatabaseTestCase(unittest.TestCase):
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

    def test_db_tables_set_up(self):
        """Ensures that the users table exists in the database."""
        self.assertTrue("users" in db.metadata.tables.keys())
