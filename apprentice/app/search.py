import requests
from elasticsearch_dsl import Document, Keyword, Short, Text
from flask import current_app, url_for
from google_images_search import GoogleImagesSearch


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

    def get_image_url(self, use_google=False):
        """Return a URL for an image of this recipe.
        It will try to return the OpenRecipes scraped image if it exists,
        else it will do a Google image search, else it will return a default
        placeholder image.

        Args:
            use_google: If true, will make an API call to Google images for missing
                images, else it will skip this step (for API quota purposes).

        Returns:
            A string URL which can be GET requested to obtain an image
        """
        # First try the OpenRecipes image
        try:
            response = requests.head(self.image, allow_redirects=True)

            if response.status_code == 200:
                return self.image
        except Exception:
            # e.g. timeout
            pass

        # Then try the first Google Image search result
        if use_google:
            try:
                google_image_search = GoogleImagesSearch(None, None)

                google_image_search.search(
                    search_params={
                        "q": self.name,
                        "num": 1,
                    }
                )

                return google_image_search.results()[0].url
            except Exception:
                # e.g. API quota limit reached
                pass

        # Else return our default image
        return url_for("static", filename="images/default_recipe_image.jpg")

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
            A list of Recipe object
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
            per_page: The size of each page of results to get.

        Returns:
            a list of Recipe objects.
        """
        return list(
            cls.search()[page * per_page : (page + 1) * per_page]
            .query("match", name=query)
            .execute()
        )

    @classmethod
    def get_recipes_by_advanced(cls, page=0, per_page=10, **criteria):
        """Advanced search wrapper for Recipes.

        An example set of criteria is as follows:
        e.g. criteria = {
            "query": "dip",
            "ingredients": ["olive oil", "garlic"],
            "calories": [0, 1000],
            "carbohydrate": [0, 100],
            "fat": [0, 100],
            "protein": [0, 100],
            "tags": ["gluten-free", "vegetarian"],
        }
        Note that all of the items are optional and will be ignored if omitted or
        if falsy values are provided (e.g. False, None, [], {}, "")

        Usage::
            >>> # e.g. direct kwargs
            >>> Recipe.get_recipes_by_advanced(query="dip", "tags"=["vegetarian"])
            >>> # e.g. splat kwargs
            >>> criteria = {"query":"dip, "tags":["vegetarian"]}
            >>> Recipe.get_recipes_by_advanced(**criteria)

        :param query: The recipe name to (partly) match
        :param page: The page of results to get
        :param per_page: The size of each page of results to get
        :param critiera: kwargs as described above
        :rtype: List[Recipe]
        """
        search = cls.search()[page * per_page : (page + 1) * per_page]

        if criteria.get("query"):
            search = search.query("match", name=criteria.get("query"))

        if criteria.get("ingredients"):
            search = search.query("terms", ingredients=criteria.get("ingredients"))

        if criteria.get("tags"):
            search = search.filter(
                "terms_set",
                tags__keyword={
                    "terms": criteria.get("tags"),
                    "minimum_should_match_script": {"source": "params.num_terms"},
                },
            )

        if criteria.get("calories"):
            min_val, max_val = criteria.get("calories")
            search = search.filter("range", calories={"gte": min_val, "lte": max_val})

        if criteria.get("carbohydrate"):
            min_val, max_val = criteria.get("carbohydrate")
            search = search.filter(
                "range", carbohydrate={"gte": min_val, "lte": max_val}
            )

        if criteria.get("fat"):
            min_val, max_val = criteria.get("fat")
            search = search.filter("range", fat={"gte": min_val, "lte": max_val})

        if criteria.get("protein"):
            min_val, max_val = criteria.get("protein")
            search = search.filter("range", protein={"gte": min_val, "lte": max_val})

        return list(search.execute())
