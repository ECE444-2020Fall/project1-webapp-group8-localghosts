import unittest

from app import create_app, db
from app.search import Recipe
from flask import current_app


class RecipeSearchTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_can_get_single_document(self):
        """Attribution (for Lab 6): Amar Arefeen"""
        self.assertEqual(type(Recipe.get_single_recipe()), Recipe)

    def test_can_get_50_recipes(self):
        """Attribution (for Lab 6): Amar Arefeen"""
        # Get 50 of them
        recipes = []
        for i in range(5):
            recipes += Recipe.get_multi_recipe_paged(page=i, per_page=10)

        # Make sure they're unique
        recipe_ids = {r.meta.id for r in recipes}
        self.assertEqual(len(recipe_ids), 50)
