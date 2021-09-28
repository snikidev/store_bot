from telegram import Update
from telegram.ext import CallbackContext
from common.send_products import send_products
from common.list_products import list_products
from loguru import logger


def inline_query(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    try:
        products = list_products()
        send_products(chat_id, context, products, inline=True)
    except Exception as e:
        logger.exception(e)