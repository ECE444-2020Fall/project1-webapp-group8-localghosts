from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, SubmitField
from wtforms.fields.html5 import IntegerField, SearchField
from wtforms.validators import DataRequired, Regexp


class Struct:
    """Utility class to help populate forms. See https://stackoverflow.com/q/35749962"""

    def __init__(self, **entries):
        self.__dict__.update(entries)


class SearchForm(FlaskForm):
    """Form for searching for a recipe."""

    query = SearchField("Recipe name", [DataRequired()], id="autocomplete", render_kw={"autocomplete": "off"})
    submit = SubmitField("Search", render_kw={"class": "btn btn-success btn-block"})


# TODO: do this properly and wire it up on the frontend
class AdvancedSearchForm(FlaskForm):
    """Forms used for the advanced search feature"""

    class RecipeForm(FlaskForm):
        """Form for searching by name and ingredients."""

        query = SearchField(
            "Recipe name",
            [DataRequired()],
            render_kw={"placeholder": "Search by recipe name"},
        )
        ingredients = FieldList(
            StringField(
                "", render_kw={"placeholder": "Search by comma-seperated ingredient(s)"}
            ),
            min_entries=1,
        )
        # https://wtforms.readthedocs.io/en/2.3.x/fields/ to make ^ look better

    class NutrientsForm(FlaskForm):
        """Form for searching by nutritional information"""

        minCalories = IntegerField(
            "Minimum Calories",
            render_kw={"placeholder": "Min"}
        )

        maxCalories = IntegerField(
            "Maximum Calories",
            render_kw={"placeholder": "Max"}
        )

        minCarbs = IntegerField(
            "Minimum Carbs",
            render_kw={"placeholder": "Min"}
        )

        maxCarbs = IntegerField(
            "Maximum Carbs",
            render_kw={"placeholder": "Max"}
        )

        minProteins = IntegerField(
            "Proteins",
            render_kw={"placeholder": "Min"}
        )

        maxProteins = IntegerField(
            "Proteins",
            render_kw={"placeholder": "Max"}
        )

        minFats = IntegerField(
            "Fats",
            render_kw={"placeholder": "Min"}
        )

        maxFats = IntegerField(
            "Fats",
            render_kw={"placeholder": "Max"}
        )


    recipe = FormField(RecipeForm)
    nutrients = FormField(NutrientsForm)
    submit = SubmitField("Search for results", render_kw={"class": "btn"})
