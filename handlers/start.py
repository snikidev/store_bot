from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from common.dictionary import dictionary


def start(update: Update, context: CallbackContext) -> None:
    language_code = update.effective_user.language_code
    chat_id = update.message.chat_id

    keyboar = [
        [dictionary[language_code].products],
        [dictionary[language_code].terms_and_conditions]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboar)

    context.bot.send_message(
        chat_id,
        dictionary[language_code].start_message,
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )