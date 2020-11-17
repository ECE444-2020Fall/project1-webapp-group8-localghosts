import requests
from flask import abort, redirect, render_template, request, session, url_for
from flask_login import login_required
from google_images_search import GoogleImagesSearch

from ..search import Recipe
from . import main
from .forms import AdvancedSearchForm, SearchForm


@main.route("/", methods=["GET", "POST"])
def index():
    """View function for the main (index) page.

    Returns:
        On a GET request, returns the rendered template for index.html
        On a POST request (search form submission), redirects to the search page, passing the form data as the query argument.
    """
    form = SearchForm()
    if request.method == "POST" or form.validate_on_submit():
        return redirect(url_for(".search", _method="GET", query=form.query.data))
    return render_template(
        "index.html",
        form=form,
        name=session.get("name"),
        known=session.get("known", False),
    )


@main.route("/search", methods=["GET", "POST"])
def search():
    """View function for the search page

    Returns:
        The rendered template search.html.

        On POST request (advanced search form submission), uses the form data for the query.
        On GET request (from index page), uses the GET request argument for the query.
    """
    form = AdvancedSearchForm()
    recipes = []

    if request.method == "GET" and "query" in request.args:
        # i.e. if coming from the index page
        recipes = Recipe.get_recipes_by_name(request.args["query"], page=0, per_page=50)
    elif request.method == "POST" or form.validate_on_submit():
        # i.e. if coming from an advanced search
        recipes = Recipe.get_recipes_by_name(
            form.recipe.query.data, page=0, per_page=50
        )

    return render_template("search.html", recipes=recipes, form=form)


@main.route("/recipe/<recipe_id>", methods=["GET", "POST"])
def recipe(recipe_id):
    """View function for recipe display

    Note: Some image URLs given by OpenRecipes are invalid. The image shown on the page is as follows:
    1. If the OpenRecipes image URL is valid, it is used.
    2. If the OpenRecipes URL is not valid, a Google Search is carried out with the recipe name, and the first image result is used.
    3. The Google API has a quota of 100 queries per day. If this limit is reached, a default image is used (from the static folder)

    Returns:
        The rendered template recipe.html for the requested recipe (by ID).
    """

    # Get recipe
    recipe = Recipe.get_recipe_by_id(recipe_id)
    if not recipe:
        abort(404)

    # Get image URL.

    # URL from openRecipes JSON
    image_url = recipe.image
    bad_url = False

    try:
        response = requests.head(image_url, allow_redirects=True)
        # If we fail to get the image from the OpenRecipes URL.
        if response.status_code != 200:
            bad_url = True

    except:
        # If getting the image throws
        bad_url = True

    # If the OpenRecipes URL is bad, use the first Google image search result
    if bad_url:

        try:

            raise Exception("blah")  # Simulate limit reached (for testing)

            google_image_search = GoogleImagesSearch(None, None)

            params = {
                "q": recipe.name,
                "num": 1,
            }

            google_image_search.search(search_params=params)

            image_url = google_image_search.results()[0].url

        # If the Google API Quota limit was reached, the search will throw.
        except:
            # Use default recipe image.
            image_url = url_for("static", filename="images/default_recipe_image.jpg")

    return render_template("recipe.html", recipe=recipe, image_url=image_url)


@main.route("/fridge", methods=["GET", "POST"])
@login_required
def fridge():
    """View function for fridge/ inventory feature

    Note: This feature is not implemented yet. fridge.html displays a "coming soon" page.

    Returns:
        The rendered template for fridge.html.
    """
    return render_template("fridge.html")


@main.route("/list", methods=["GET", "POST"])
@login_required
def list():
    """View function for grocery list feature

    Note: This feature is not implemented yet. list.html displays a "coming soon" page.

    Returns:
        The rendered template for list.html
    """
    return render_template("list.html")
