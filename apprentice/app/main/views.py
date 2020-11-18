from flask import abort, redirect, render_template, request, session, url_for
from flask_login import login_required

from ..search import Recipe
from . import main
from .forms import AdvancedSearchForm, SearchForm, Struct


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
@main.route("/search/<int:page>/", methods=["GET", "POST"])
def search(page=0):
    """View function for the search page

    Args:
        page: page of results to return, default is 0th page
        request.args: any of the search criteria dictionary
    Returns:
        The rendered template search.html.

        On POST request (advanced search form submission), redirects back to a GET request.
        On GET request (from index page), uses the GET request argument for the query.
    """
    form = AdvancedSearchForm()
    if request.method == "POST" or form.validate_on_submit():
        return redirect(
            url_for(
                ".search",
                _method="GET",
                query=form.recipe.query.data,
                ingredients=form.recipe.ingredients.data,
                calories=form.nutrients.calories.data,
                carbohydrate=form.nutrients.carbs.data,
                fat=form.nutrients.fats.data,
                protein=form.nutrients.protein.data,
            )
        )

    # Populate form data from before if available
    form.recipe.form.populate_obj(
        Struct(
            query=request.args.get("query"),
            ingredients=request.args.get("ingredients"),
        )
    )
    form.nutrients.form.populate_obj(
        Struct(
            calories=request.args.get("calories"),
            carbs=request.args.get("carbohydrate"),
            fats=request.args.get("fat"),
            protein=request.args.get("protein"),
        )
    )

    # Populate recipes
    criteria = {
        "query": request.args.get("query"),
        "ingredients": request.args.get("ingredients"),
        "calories": request.args.get("calories"),
        "carbohydrate": request.args.get("carbohydrate"),
        "fat": request.args.get("fat"),
        "protein": request.args.get("protein"),
    }
    recipe_search = Recipe.get_recipes_by_criteria(
        page=page,
        per_page=8,
        **criteria,
    )

    try:
        recipe_search_results = recipe_search.execute()
        recipes = list(recipe_search_results)
        total_results = recipe_search_results.hits.total.value
    except:
        recipes = []
        total_results = 0
    return render_template(
        "search.html",
        recipes=recipes,
        total_results=total_results,
        form=form,
    )


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

    return render_template(
        "recipe.html", recipe=recipe, image_url=recipe.get_image_url(use_google=True)
    )


@main.route("/fridge", methods=["GET", "POST"])
@login_required
def fridge():
    """View function for fridge/ inventory feature

    Note: This feature is not implemented yet. fridge.html displays a "coming soon" page.

    Returns:
        The rendered template for fridge.html.
    """
    return render_template("fridge.html")


@main.route("/grocerylist", methods=["GET", "POST"])
@login_required
def grocerylist():
    """View function for grocerylist feature

    Note: This feature is not implemented yet. grocerylist.html displays a "coming soon" page.

    Returns:
        The rendered template for grocerylist.html
    """
    return render_template("grocerylist.html")
