from elasticsearch_dsl import Document, Keyword, Short, Text
from elasticsearch_dsl.response import Response
from flask import current_app


class Recipe(Document):
    """Python representation of a Recipe document in Elasticsearch

    :param name: A string, the recipe title.
    :param ingredients: A list of strings, the ingredients of the recipe.
    :param url: A string, the URL from where the recipe was sourced
    :param source: A string, the original publisher of the recipe

    :param calories: An int, the calorie count of the recipe. randint(0, 2000)
    :param carbohydrate: An int, the carb count of the recipe. randint(0, 75)
    :param fat: An int, the fat count of the recipe. randint(0, 100)
    :param protein: An int, the protein count of the recipe. randint(0, 50)

    :param image: A optional string, the URL for an image of the recipe
    :param cookTime: An optional string, the cook time
    :param recipeYield: An optional string, the recipe yield
    :param datePublished: An optional string, the original publish date
    :param prepTime: An optional string, the prep time
    :param description: An optional string, the recipe pretext/description
    :param totalTime: An optional string, the total cook/prep time
    :param creator: An optional string, the original author of the recipe
    :param recipeCategory: An optional string, the type of recipe
    :param recipeInstructions: An optional string, the recipe instructions
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

    # The Index inner class is where we define connection config
    class Index:
        name = "recipes"

    @classmethod
    def _get_using(cls, using=None):
        """Override base method for specifying our current Elasticsearch connection"""
        return current_app.elasticsearch

    ### THESE ARE SAMPLE METHODS FOR YOU TO GET DATA FROM ###

    @classmethod
    def get_single_recipe(cls):
        """Return a single Recipe object from Elasticsearch

        :rtype: Recipe
        """
        return cls.search().execute()[0]

    @classmethod
    def get_multi_recipe_paged(cls, page=0, per_page=10):
        """Return a list of Recipes, considering pagination

        Usage::

            >>> # Default options just get you the first 10 recipes
            >>> recipes_0 = Recipe.get_multi_recipe_paged() #page=0
            >>> # Get next set of results by specifying the page
            >>> recipes_1 = Recipe.get_multi_recipe_paged(page=1)
            >>> # Get more results by changing page size
            >>> recipes_0_4 = Recipe.get_multi_recipe_paged(per_page=50)

        :param page: The page of results to get
        :param per_page: The size of each page of results to get
        :rtype: List[Recipe]
        """
        return list(cls.search()[page * per_page : (page + 1) * per_page].execute())

    ### TODO: CUSTOM SEARCH METHODS ###
    @classmethod
    def get_recipe_by_id(cls, recipe_id):
        """Return a single Recipe object from Elasticsearch by it's ID

        :rtype: Recipe, or None if not found
        """
        try:
            return cls.get(recipe_id)
        except Exception:
            return None

    @classmethod
    def get_recipes_by_name(cls, query, page=0, per_page=10):
        """Return a list of Recipes, considering pagination, whose names
        match the provided query

        :param query: The recipe name to (partly) match
        :param page: The page of results to get
        :param per_page: The size of each page of results to get
        :rtype: List[Recipe]
        """
        return list(
            cls.search()[page * per_page : (page + 1) * per_page]
            .query("match", name=query)
            .execute()
        )
