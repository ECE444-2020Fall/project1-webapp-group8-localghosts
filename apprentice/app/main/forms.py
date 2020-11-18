from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, SubmitField
from wtforms.fields.html5 import IntegerField, SearchField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    """Form for searching for a recipe."""

    query = SearchField("Recipe name", [DataRequired()])
    submit = SubmitField("Search", render_kw={"class": "btn btn-success btn-block"})


# TODO: do this properly and wire it up on the frontend 
class AdvancedSearchForm(FlaskForm):
    """Forms used for the advanced search feature"""

    class RecipeForm(FlaskForm):
        """Form for searching by name and ingredients."""     
        query = SearchField("Recipe name", [DataRequired()],  render_kw={"placeholder": "Search by recipe name"})
        ingredients = FieldList(StringField("", render_kw={"placeholder": "Search by ingredient(s)"}), min_entries=1)
        # https://wtforms.readthedocs.io/en/2.3.x/fields/ to make ^ look better
    class NutrientsForm(FlaskForm):
        """Form for searching by nutritional information"""

        calories = IntegerField("Calories")
        carbs = IntegerField("Carbs")
        fats = IntegerField("Fats")
        protein = IntegerField("Protein")

    recipe = FormField(RecipeForm)
    nutrients = FormField(NutrientsForm)
    submit = SubmitField("Search for results",  render_kw={"class": "btn"})
