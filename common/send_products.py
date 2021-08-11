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
                currency=product.currency,
                description=product.description,
                is_flexible=product.is_flexible,
                need_email=product.need_email,
                payload=product.invoice_payload,
                photo_height=product.photo_height,
                photo_size=product.photo_size,
                photo_url=product.photo_url,
                photo_width=product.photo_width,
                prices=product.prices,
                provider_token=product.provider_token,
                send_email_to_provider=product.send_email_to_provider,
                title=product.title,
            )

            products_for_inline.append(
                InlineQueryResultArticle(
                    id=product.invoice_payload,
                    input_message_content=input_message_content,
                    thumb_url=product.photo_url,
                    title=product.title,
                )
            )

        bot.answer_inline_query(message.id, products_for_inline)

    else:
        for product in product_list:
            bot.send_invoice(message.chat.id, **product.dict())
