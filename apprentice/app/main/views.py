import json
import os

from flask import (
    abort,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required

from .. import db
from ..models import User
from ..search import Recipe
from . import main
from .forms import AdvancedSearchForm, SearchForm


@main.route("/", methods=["GET", "POST"])
def index():
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
    """
    Returns the rendered template search.html

       The search page will display recipes from the database given a query in the search box

       Note: for now the search will only display 'search results' as cards for display
       No query is given yet
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
    recipe = Recipe.get_recipe_by_id(recipe_id)
    if not recipe:
        abort(404)
    return render_template("recipe.html", recipe=recipe)


@main.route("/fridge", methods=["GET", "POST"])
@login_required
def fridge():
    return render_template("fridge.html")


@main.route("/list", methods=["GET", "POST"])
@login_required
def list():
    return render_template("list.html")
