from elasticsearch_dsl import Document, Keyword, Short, Text
from flask import current_app, url_for


class Recipe(Document):
    """Python representation of a Recipe document in Elasticsearch.

    Args:
        name: A string, the recipe title.
        ingredients: A list of strings, the ingredients of the recipe.
        url: A string, the URL from where the recipe was sourced
        source: A string, the original publisher of the recipe

        calories: An int, the calorie count of the recipe. randint(0, 1400)
        carbohydrate: An int, the carb count of the recipe. randint(0, 75)
        fat: An int, the fat count of the recipe. randint(0, 100)
        protein: An int, the protein count of the recipe. randint(0, 50)

        image: A optional string, the URL for an image of the recipe
        cookTime: An optional string, the cook time
        recipeYield: An optional string, the recipe yield
        datePublished: An optional string, the original publish date
        prepTime: An optional string, the prep time
        description: An optional string, the recipe pretext/description
        totalTime: An optional string, the total cook/prep time
        creator: An optional string, the original author of the recipe
        recipeCategory: An optional string, the type of recipe
        recipeInstructions: An optional string, the recipe instructions
        tags: An optional string array containing any of ["vegetarian", "vegan", "gluten-free"]
    """

    # These fields should be identical to those in recipe-db/loading-scripts/recipe-mapping.json
    name = Text(fields={"keyword": Keyword()})
    ingredients = Text(fields={"keyword": Keyword()})
    url = Text(fields={"keyword": Keyword()})
    source = Text(fields={"keyword": Keyword()})
    calories = Short()
    carbohydrate = Short()
    fat = Short()
    protein = Short()
    image = Text(fields={"keyword": Keyword()})
    cookTime = Text(fields={"keyword": Keyword()})
    recipeYield = Text(fields={"keyword": Keyword()})
    datePublished = Text(fields={"keyword": Keyword()})
    prepTime = Text(fields={"keyword": Keyword()})
    description = Text(fields={"keyword": Keyword()})
    totalTime = Text(fields={"keyword": Keyword()})
    creator = Text(fields={"keyword": Keyword()})
    recipeCategory = Text(fields={"keyword": Keyword()})
    recipeInstructions = Text(fields={"keyword": Keyword()})
    tags = Text(fields={"keyword": Keyword()})

    # The Index inner class is where we define connection config
    class Index:
        name = "recipes"

    @classmethod
    def _get_using(cls, using=None):
        """Override base method for specifying our current Elasticsearch connection"""
        return current_app.elasticsearch

    # THESE ARE SAMPLE METHODS FOR YOU TO GET DATA FROM

    @classmethod
    def get_single_recipe(cls):
        """Return a single Recipe object from Elasticsearch

        Returns:
            A Recipe object.
        """
        return cls.search().execute()[0]

    @classmethod
    def get_multi_recipe_paged(cls, page=0, per_page=10):
        """Return a list of Recipes, considering pagination

        Usage:

            >>> # Default options just gets you the first 10 recipes
            >>> recipes_0 = Recipe.get_multi_recipe_paged() #page=0
            >>> # Get next set of results by specifying the page
            >>> recipes_1 = Recipe.get_multi_recipe_paged(page=1)
            >>> # Get more results by changing page size
            >>> recipes_0_4 = Recipe.get_multi_recipe_paged(per_page=50)

        Args:
            page: The page of results to get
            per_page: The size of each page of results to get

        Returns:
            A list of Recipe objects
        """
        return list(cls.search()[page * per_page : (page + 1) * per_page].execute())

    # TODO: CUSTOM SEARCH METHODS
    @classmethod
    def get_recipe_by_id(cls, recipe_id):
        """Return a single Recipe object from Elasticsearch by its ID

        Args:
            recipe_id: The ID of the recipe to get.

        Returns:
            The Recipe object corresponding to the given ID, or None if not found
        """
        try:
            return cls.get(recipe_id)
        except Exception:
            return None

    @classmethod
    def get_recipes_by_name(cls, query, page=0, per_page=10):
        """Return a list of Recipes, considering pagination, whose names
        match the provided query

        Args:
            query: The recipe name to (partly) match
            page: The page of results to get
            per_page: The size of each page of results to get

        Returns:
            a list of Recipe objects
        """
        return list(
            cls.search()[page * per_page : (page + 1) * per_page]
            .query("match", name=query)
            .execute()
        )

