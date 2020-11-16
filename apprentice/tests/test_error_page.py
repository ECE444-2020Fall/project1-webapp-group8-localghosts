import unittest

from app import create_app, db


class ErrorPageTestCase(unittest.TestCase):
    def setUp(self):
        """Setup app context and database
        """
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Ends session and drops database
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def testErrorPage(self):
        """Checks that a 404 error code is returned when a page is not found
        """
        response = self.app.test_client().get("/blurr")
        self.assertEqual(response.status_code, 404)
