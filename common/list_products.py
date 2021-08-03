import requests
from common.settings import Settings
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
    return mapped_products
