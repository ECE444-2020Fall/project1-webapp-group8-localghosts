import unittest

from app import create_app, db
from app.search import Recipe


class RecipeSearchTestCase(unittest.TestCase):
    def setUp(self):
        """Setup app context and database"""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Ends session and drops database"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_can_get_single_document(self):
        """Ensures that the get_single_recipe fucntion returns a Recipe object"""
        self.assertEqual(type(Recipe.get_single_recipe()), Recipe)

    def test_can_get_50_recipes(self):
        """Ensures that the get_multi_recipe_paged function works as expected"""

        # Get 50 of them
        recipes = []
        for i in range(5):
            recipes += Recipe.get_multi_recipe_paged(page=i, per_page=10)

        # Make sure they're unique
        recipe_ids = {r.meta.id for r in recipes}
        self.assertEqual(len(recipe_ids), 50)

    def test_get_recipe_by_id(self):
        """Asserts the functionality of getting a recipe by ID."""
        recipe_1 = Recipe.get_single_recipe()
        recipe_2 = Recipe.get_recipe_by_id(recipe_1.meta.id)
        self.assertEqual(recipe_1, recipe_2)

    def test_get_recipes_by_name(self):
        """Asserts the functionality of getting a recipe by name."""
        # Check that it finds stuff that exists
        for query in ["chicken", "salad"]:
            results = Recipe.get_recipes_by_name(query, per_page=5)
            for result in results:
                self.assertIn(query, result.name.lower())

        # Check that it doesn't find stuff that doesn't exist
        self.assertFalse(
            Recipe.get_recipes_by_name("somethingthatdefinitelydoesnotexist")
        )
