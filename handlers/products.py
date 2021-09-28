from telegram import Update
from telegram.ext import CallbackContext
from common.dictionary import dictionary
from common.send_products import send_products
from common.list_products import list_products
from loguru import logger

def products_handler(update: Update, context: CallbackContext) -> None:
    language_code = update.effective_user.language_code
    chat_id = update.message.chat_id

    try:
        products = list_products()
        send_products(chat_id, context, products)

    except Exception as e:
        logger.exception(e)
        context.bot.send_message(
            chat_id,
            dictionary[language_code].get_products_error,
        )