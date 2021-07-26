def send_products(bot, message, products):
    product_list = list(products)
    for product in product_list:
        bot.send_invoice(message.chat.id, **product.dict())
