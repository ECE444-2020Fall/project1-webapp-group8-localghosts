import gzip
import json
import random
from io import BytesIO
from typing import List
from urllib.request import urlopen

from elasticsearch import Elasticsearch, helpers

RECIPES_URL = "https://s3.amazonaws.com/openrecipes/20170107-061401-recipeitems.json.gz"
ES_URL = "http://localhost:9200"

ES_INDEX = "recipes"
ES_MAPPING = {}  # will load from ./recipe-mapping.json


def download_file(url: str): -> List[dict]:
    recipes = []
    with urlopen(url) as f:
        with gzip.GzipFile(fileobj=BytesIO(f.read())) as g:
            for line in g:
                recipes.append(json.loads(line))

    return recipes


def process_recipe(recipe: dict):  -> dict:
    # Remove unwanted fields
    for key, value in list(recipe.items()):
        if key not in ES_MAPPING["properties"] or value is None:
            del recipe[key]

    # Split ingredients into an array
    recipe["ingredients"] = recipe["ingredients"].split("\n")

    # Add nutritional information; random data for now ¯\_(ツ)_/¯
    recipe.update(
        calories=random.randint(0, 2000),
        carbohydrate=random.randint(0, 75),
        fat=random.randint(0, 100),
        protein=random.randint(0, 50),
    )

    # TODO: additional processing?

    return recipe


def load_elastic(index: str, mapping: dict, docs: List[dict]):
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
