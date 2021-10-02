from telegram.ext import CallbackContext
from loguru import logger
from telegram import (
    InlineQueryResultArticle,
    InputInvoiceMessageContent,
)


def send_products(update, context: CallbackContext, products, inline=False):
    product_list = list(products)
    if inline:
        products_for_inline = []

        for product in product_list:
            input_message_content = InputInvoiceMessageContent(
                currency=product.currency,
                description=product.description,
                is_flexible=product.is_flexible,
                need_email=product.need_email,
                payload=product.payload,
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
                    id=product.payload,
                    input_message_content=input_message_content,
                    thumb_url=product.photo_url,
                    title=product.title,
                )
            )

        update.inline_query.answer(products_for_inline)
    else:
        chat_id = update.message.chat_id
        for product in product_list:
            context.bot.send_invoice(chat_id, **product.dict())
