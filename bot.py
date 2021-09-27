from dotenv import load_dotenv

load_dotenv()

import common.sentry, logging, telebot
from common.settings import Settings
from common.send_products import send_products
from common.list_products import list_products
from common.send_deliverables import send_deliverables
from common.dictionary import dictionary
from loguru import logger
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from helpers.formatters import escape_markdown_chars

settings = Settings()
bot = telebot.TeleBot(settings.bot_token, parse_mode="Markdown")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    language_code = message.from_user.language_code

    markup = ReplyKeyboardMarkup(row_width=1)
    terms_button = KeyboardButton(dictionary[language_code].terms_and_conditions)
    products_button = KeyboardButton(dictionary[language_code].products)

    markup.add(products_button, terms_button)

    bot.send_message(
        message.chat.id,
        dictionary[language_code].start_message,
        parse_mode="Markdown",
        reply_markup=markup,
    )


@bot.message_handler(
    func=lambda message: message.text == dictionary["en"].products
    or message.text == dictionary["ru"].products
)
def handle_send_products(message):
    language_code = message.from_user.language_code

    try:
        products = list_products()
        send_products(bot, message, products)

    except Exception as e:
        logger.exception(e)
        bot.send_message(
            message.chat.id,
            dictionary[language_code].get_products_error,
        )


# TODO: double check this
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    logging.info("pre_checkout_query")
    logging.info(pre_checkout_query)

    language_code = pre_checkout_query.from_user.language_code

    bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True,
        error_message=dictionary[language_code].pre_checkout_error,
    )


@bot.message_handler(content_types=["successful_payment"])
def got_payment(message):
    language_code = message.from_user.language_code
    order_number = escape_markdown_chars(
        message.successful_payment.provider_payment_charge_id
    )

    message_text = dictionary[language_code].success_message.format(order_number)

    bot.send_message(message.chat.id, message_text)
    send_deliverables(bot, message)


@bot.message_handler(
    func=lambda message: message.text == dictionary["en"].terms_and_conditions
    or message.text == dictionary["ru"].terms_and_conditions
)
def command_terms(message):
    language_code = message.from_user.language_code

    bot.send_message(
        message.chat.id, dictionary[language_code].terms_and_conditions_text
    )


@bot.inline_handler(lambda query: len(query.query) == 0)
def query_all_products(inline_query):
    try:
        products = list_products()
        send_products(bot, inline_query, products, inline=True)
    except Exception as e:
        logger.exception(e)


bot.skip_pending = True

bot.infinity_polling()
