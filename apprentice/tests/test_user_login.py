import unittest

from app import create_app, db
from app.models import User


class UserLoginTestCase(unittest.TestCase):
    def setUp(self):
        """Setup app context and database"""
        self.app = create_app("testing")
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Ends session and drops database"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_navbar_buttons_logged_out(self):
        """Ensures that "Login" and "Sign Up" are in the navbar when user is logged out."""
        response = self.app.test_client().get("/")
        self.assertTrue(b"Login" in response.data)
        self.assertTrue(b"Sign up" in response.data)
        self.assertEqual(response.status_code, 200)

    def test_database_add_user(self):
        """Ensures that a user can be added to the database."""
        user = User(
            email="test@hotmail.com",
            username="testuser",
            password="mypassword",
        )
        db.session.add(user)
        db.session.commit()

        result = User.query.filter_by(email="test@hotmail.com").first()
        self.assertFalse(result is None)
        self.assertTrue(result.username == "testuser")

    def test_login_user_does_not_exist(self):
        """Ensures that a user is not logged in on an attempt to login with a non-existent user."""
        response = self.app.test_client().post(
            "/auth/login",
            data=dict(email="idontexist@hotmail.com", password="password"),
        )
        self.assertFalse(b"Sign Out" in response.data)
        self.assertTrue(b"Login" in response.data)
        self.assertEqual(response.status_code, 200)

    def test_login_user_exists(self):
        """Ensures that a user is logged in when login information is valid.
        Checks that the navigation bar content is adjusted as expected.
        """
        response = self.app.test_client().post(
            "/auth/signup",
            data=dict(
                username="helloworld",
                email="test@hotmail.com",
                password="topsecret",
                password2="topsecret",
            ),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        response = self.app.test_client().post(
            "/auth/login",
            data=dict(email="test@hotmail.com", password="topsecret"),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Sign Out" in response.data)
        self.assertTrue(b"Signed in as helloworld" in response.data)

    def test_login_wrong_password(self):
        """Ensures that a user is not logged in if the wrong password is provided"""
        response = self.app.test_client().post(
            "/auth/signup",
            data=dict(
                username="helloworld",
                email="test@hotmail.com",
                password="topsecret",
                password2="topsecret",
            ),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        response = self.app.test_client().post(
            "/auth/login",
            data=dict(email="test@hotmail.com", password="thisiswrong"),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(b"Sign Out" in response.data)
        self.assertTrue(b"Login" in response.data)

    def test_logout(self):
        """Ensures that user logout works as expected."""
        response = self.app.test_client().post(
            "/auth/signup",
            data=dict(
                username="helloworld",
                email="test@hotmail.com",
                password="topsecret",
                password2="topsecret",
            ),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        response = self.app.test_client().post(
            "/auth/login",
            data=dict(email="test@hotmail.com", password="topsecret"),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Sign Out" in response.data)
        self.assertTrue(b"Signed in as helloworld" in response.data)

        response = self.app.test_client().get("/auth/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(b"Sign Out" in response.data)
        self.assertTrue(b"Login" in response.data)
