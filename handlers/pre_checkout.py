from telegram import Update


def pre_checkout(update: Update) -> None:
    query = update.pre_checkout_query
    query.answer(ok=True)
