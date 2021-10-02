from telegram import Update
from telegram.ext import CallbackContext
from common.send_products import send_products
from common.list_products import list_products
from loguru import logger


def inline_query(update: Update, context: CallbackContext) -> None:
    try:
        products = list_products()
        send_products(update, context, products, inline=True)
    except Exception as e:
        logger.exception(e)