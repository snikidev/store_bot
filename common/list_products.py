import requests
from common.settings import Settings
from helpers.mappers import map_products

settings = Settings()


def list_products():
    url = settings.airtable_api_url + f"?api_key={settings.airtable_api_key}"
    products = requests.request("GET", url).json()
    mapped_products = map_products(products["records"])

    return mapped_products
