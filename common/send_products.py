from telebot import TeleBot
from telebot.types import (
    InlineQueryResultArticle,
    InputInvoiceMessageContent,
)


def send_products(bot: TeleBot, message, products, inline=False):
    product_list = list(products)
    if inline:
        products_for_inline = []

        for product in product_list:
            input_message_content = InputInvoiceMessageContent(
                title=product.title,
                description=product.description,
                provider_token=product.provider_token,
                currency=product.currency,
                payload=product.invoice_payload,
                prices=product.prices,
                photo_url=product.photo_url,
                photo_size=product.photo_size,
                photo_width=product.photo_width,
                photo_height=product.photo_height,
                is_flexible=product.is_flexible,
            )

            products_for_inline.append(
                InlineQueryResultArticle(
                    id=product.invoice_payload,
                    title=product.title,
                    input_message_content=input_message_content,
                    thumb_url=product.photo_url,
                )
            )

        bot.answer_inline_query(message.id, products_for_inline)

    else:
        for product in product_list:
            bot.send_invoice(message.chat.id, **product.dict())
