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
            results = list(
                Recipe.get_recipes_by_criteria(query=query, per_page=5).execute()
            )
            for result in results:
                self.assertIn(query, result.name.lower())

        # Check that it doesn't find stuff that doesn't exist
        self.assertFalse(
            list(
                Recipe.get_recipes_by_criteria(
                    query="somethingthatdefinitelydoesnotexist"
                ).execute()
            )
        )

    def test_advanced_search(self):
        """Asserts the functionality of getting a recipe with many criteria"""
        criteria = {
            "query": "dip",
            "ingredients": "olive oil, garlic",
            "tags": ["gluten-free", "vegetarian"],
            "minCalories": 0,
            "maxCalories": 100,
            "minCarbs": 0,
            "maxCarbs": 100,
            "minProteins": 0,
            "maxProteins": 100,
            "minFats": 0,
            "maxFats": 100,
        }

        search = Recipe.get_recipes_by_criteria(**criteria)
        results = list(search.execute())
        self.assertTrue(results)
        for result in results:
            self.assertIn(criteria["query"], result.name.lower())

            # Ingredients are an any-match
            ingredients_match = False
            for ingredient in criteria["ingredients"].split(","):
                ingredients_match |= any(
                    ingredient in src.lower() for src in result.ingredients
                )
            self.assertTrue(ingredients_match)

            # Tags are an all-match
            for tag in criteria["tags"]:
                self.assertIn(tag, result.tags)

            self.assertIn(
                result.calories,
                range(criteria["minCalories"], criteria["maxCalories"] + 1),
            )
            self.assertIn(
                result.carbohydrate,
                range(criteria["minCarbs"], criteria["maxCarbs"] + 1),
            )
            self.assertIn(
                result.fat, range(criteria["minFats"], criteria["maxFats"] + 1)
            )
            self.assertIn(
                result.protein,
                range(criteria["minProteins"], criteria["maxProteins"] + 1),
            )

    def test_recipe_suggestions(self):
        for query in ["chicken", "salad"]:
            results = list(Recipe.get_recipe_suggestions(query).execute())
            for result in results:
                self.assertIn(query, result.name.lower())


class RecipeSearchRenderTestCase(unittest.TestCase):
    """
    app_1      | app/main/views.py                          52     25    52%   19, 31-32, 49-130, 174, 187
    """

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

    def test_simple_search(self):
        # GET the page
        response = self.app.test_client().get("/")
        self.assertEqual(response.status_code, 200)
        # POST a search
        response = self.app.test_client().post(
            "/",
            data=dict(query="test"),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_advanced_search(self):
        # GET the page
        response = self.app.test_client().get("/search")
        self.assertEqual(response.status_code, 200)
        # POST a search
        response = self.app.test_client().post(
            "/search",
            data=dict(query="test", tags="vegetarian"),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_autocomplete_suggestions(self):
        # GET the page
        response = self.app.test_client().get("/search/autocomplete?query=chicken")
        self.assertGreaterEqual(len(response.data), len("[]"))
