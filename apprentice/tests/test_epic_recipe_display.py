import unittest

from app import create_app, db
from app.search import Recipe
from flask import current_app


class RecipeDisplayTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        # TODO: replace -- this is a dummy test
        self.assertFalse(current_app is None)
    
    def test_recipe_exists(self):
        recipe = Recipe.get_single_recipe()
        response = self.app.test_client().get(
            f"/recipe/{recipe.meta.id}"
        )
        self.assertEqual(response.status_code, 200)

    def test_recipe_not_exists(self):
        response = self.app.test_client().get(
            "/recipe/this-definitely-does-not-exist-in-the-database"
        )
        self.assertEqual(response.status_code, 404)
