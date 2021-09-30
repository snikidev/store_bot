from telegram import Update
from telegram.ext import CallbackContext


def pre_checkout(update: Update, context: CallbackContext) -> None:
    query = update.pre_checkout_query
    query.answer(ok=True)
