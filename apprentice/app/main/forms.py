from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, SubmitField
from wtforms.fields.html5 import IntegerField, SearchField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    query = SearchField("Recipe name", [DataRequired()])
    submit = SubmitField("Search", render_kw={"class": "btn btn-success btn-block"})


# TODO: do this properly and wire it up on the frontend
class AdvancedSearchForm(FlaskForm):
    class RecipeForm(FlaskForm):
        query = SearchField("Recipe name", [DataRequired()])
        ingredients = FieldList(StringField("Ingredient"), min_entries=1)

    class NutrientsForm(FlaskForm):
        calories = IntegerField("Calories")
        carbs = IntegerField("Carbs")
        fats = IntegerField("Fats")
        protein = IntegerField("Protein")

    recipe = FormField(RecipeForm)
    nutrients = FormField(NutrientsForm)
    submit = SubmitField("Search", render_kw={"class": "btn btn-success btn-block"})
