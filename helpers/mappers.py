from models.product import Product


def map_products(products):
    mapped_products = []
    for product in products:
        id, fields = product["id"], product["fields"]
        keys = list(fields.keys())

        if (
            "title" in keys
            and "description" in keys
            and "files" in keys
            and "price" in keys
            and "photo" in keys
        ):
            mapped_products.append(Product(id=id, **fields))

        continue
    return mapped_products
