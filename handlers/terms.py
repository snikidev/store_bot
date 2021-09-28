from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from common.dictionary import dictionary


def terms(update: Update, context: CallbackContext) -> None:
    language_code = update.effective_user.language_code
    chat_id = update.message.chat_id

    context.bot.send_message(
        chat_id,
        dictionary[language_code].terms_and_conditions_text,
        parse_mode=ParseMode.MARKDOWN,
    )
