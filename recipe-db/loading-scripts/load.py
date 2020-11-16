import gzip
import json
import random
import re
from io import BytesIO
from typing import List
from urllib.request import urlopen

from elasticsearch import Elasticsearch, helpers

# INPUT CONSTANTS
RECIPES_URL = "https://s3.amazonaws.com/openrecipes/20170107-061401-recipeitems.json.gz"

# PROCESSING CONSTANTS
# These constants are just for demo purposes, in reality we would have to manually
# check each and every recipe to ensure their correctness.
RE_GLUTEN_FREE = re.compile(
    "|".join(
        [
            "bagel",
            "barley",
            "bread",
            "cake",
            "flour",
            "gluten",
            "loaf",
            "muffin",
            "rye",
            "wheat",
        ]
    ),
    re.IGNORECASE,
)
# Inspired by https://github.com/imsky/wordlists/blob/master/nouns/meat.txt
RE_VEGETARIAN = re.compile(
    "|".join(
        [
            "alligator",
            "beef",
            "bison",
            "buffalo",
            "caribou",
            "chicken",
            "duck",
            "elk",
            "fish",
            "goat",
            "ham",
            "lamb",
            "pheasant",
            "pepperoni",
            "pork",
            "prawn",
            "quail",
            "rabbit",
            "salami",
            "shrimp",
            "salmon",
            "steak",
            "turkey",
            "tuna",
            "veal",
            "venison",
            "yak",
        ]
    ),
    re.IGNORECASE,
)
RE_VEGAN = re.compile("|".join(["milk", "cream", "cheese", "egg"]), re.IGNORECASE)

# OUTPUT CONSTANTS
ES_INDEX = "recipes"
ES_MAPPING = {}  # will load from ./recipe-mapping.json


def download_file(url: str) -> List[dict]:
    """Reads the openRecipes json and converts it to a list of recipes (python dicts)

    Args:
        url: A string with the url of the openRecipes json.

    Returns:
        A list of recipes (python  dictionaries) read from the json.
    """
    recipes = []
    with urlopen(url) as f:
        with gzip.GzipFile(fileobj=BytesIO(f.read())) as g:
            for line in g:
                recipes.append(json.loads(line))

    return recipes


def process_recipe(recipe: dict) -> dict:
    """Processes a recipe (dictionary):
    - Removes unwanted fields
    - Adds tags for dietary restrictions
    - Converts ingredients into an array
    - Adds Nutritional Information data

    Args:
        recipe: A python dictionary representing the recipe to be processed
    Return:
        A updated python dictionary for the processed recipe information
    """
    # Remove unwanted fields
    for key, value in list(recipe.items()):
        if key not in ES_MAPPING["properties"] or value is None:
            del recipe[key]

    # Apply tags depending on recipe content
    tags = []
    body = recipe["name"] + recipe["ingredients"]
    if not RE_GLUTEN_FREE.search(body):
        tags.append("gluten-free")
    if not RE_VEGETARIAN.search(body):
        tags.append("vegetarian")
        if not RE_VEGAN.search(body):
            tags.append("vegan")  # treat as subset of vegetarian
    if tags:
        recipe["tags"] = tags

    # Split ingredients into an array
    recipe["ingredients"] = recipe["ingredients"].split("\n")

    # Add nutritional information; random data for now ¯\_(ツ)_/¯
    recipe.update(
        carbohydrate=random.randint(0, 75),
        fat=random.randint(0, 100),
        protein=random.randint(0, 50),
    )

    # https://www.nal.usda.gov/fnic/how-many-calories-are-one-gram-fat-carbohydrate-or-protein
    recipe["calories"] = 9 * recipe["fat"] + 4 * (
        recipe["carbohydrate"] + recipe["protein"]
    )

    return recipe


def load_elastic(index: str, mapping: dict, docs: List[dict]):
    """Loads a list of python dicts into elastic search.

    Args:
        index: The elasticsearch index to load into ("recipes" in our case)
        mapping: The elasticsearch mapping to use (in our case this will load from ./recipe-mapping.json)
        docs: The data (list of dictionaries) to load into elastic search. In our case, this is the processed recipe information.
    """
    # Connect to Elastic and (re)create index
    elastic_client = Elasticsearch(
        [{"host": "localhost", "port": "9200"}], max_retries=10, retry_on_timeout=True
    )

    if elastic_client.indices.exists(ES_INDEX):
        elastic_client.indices.delete(ES_INDEX)
    elastic_client.indices.create(ES_INDEX, body={"mappings": ES_MAPPING})

    # Push docs to Elastic
    successes, failures = helpers.bulk(
        elastic_client,
        ({"_index": ES_INDEX, "_source": doc} for doc in docs),
        chunk_size=10000,
        stats_only=True,
        raise_on_exception=False,
        raise_on_error=False,
    )
    if failures:
        logging.error(f"Sent {successes} docs to {ES_INDEX} with {failures} failures")
    else:
        logging.info(f"Sent {successes} docs to {ES_INDEX} with no failures")


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)

    logging.info("Loading configuration...")

    random.seed(0)  # for the nutritional info we're generating
    with open("./recipe-mapping.json") as f:
        ES_MAPPING.update(json.load(f))

    logging.info("Downloading recipe dump...")
    recipes = download_file(RECIPES_URL)

    logging.info("Processing recipes...")
    recipes = [process_recipe(r) for r in recipes]

    logging.info("Sending to Elastic...")
    load_elastic(index=ES_INDEX, mapping=ES_MAPPING, docs=recipes)

    logging.info("Finished.")
