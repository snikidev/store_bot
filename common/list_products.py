import requests
from loguru import logger
from common.settings import Settings
from models.product import Product
from helpers.mappers import map_products

settings = Settings()

url = 'https://api.chec.io/v1/products'
params = {
    'limit': '25',
}
headers = {
    'X-Authorization': settings.commercejs_token
}


def list_products():
    products = requests.request(
        'GET', url, headers=headers, params=params).json()
    mapped_products = map(map_products, products['data'])
    # TO ASK: we need to document what we're returning here, right?
    #         how do we know what's returned here otherwise?
    return mapped_products
