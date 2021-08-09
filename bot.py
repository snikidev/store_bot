from dotenv import load_dotenv

load_dotenv()

import common.sentry
from common.settings import Settings
from common.send_products import send_products
from common.list_products import list_products
from common.send_deliverables import send_deliverables
from loguru import logger
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

settings = Settings()
bot = telebot.TeleBot(settings.bot_token, parse_mode="Markdown")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=1)
    terms_button = KeyboardButton("📜 Terms / Условия")
    products_button = KeyboardButton("🛍 Products / Продукты")
    markup.add(products_button, terms_button)

    bot.send_message(
        message.chat.id,
        "Hi, and welome to the store!👋 Check out what we currently have on sale. Cheers! 🙌",
        parse_mode="Markdown",
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text == "🛍 Products / Продукты")
def handle_send_products(message):
    try:
        products = list_products()
        send_products(bot, message, products)

    except Exception as e:
        logger.exception(e)
        bot.send_message(
            message.chat.id,
            """🇬🇧 Oops, something went wrong... Try getting the products again.  
            🇷🇺 Упс, что-то пошло не так... Попробуйте заного запросить продукты. 
            """,
        )


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True,
        error_message="""🇬🇧 Oops, something went wrong... We couldn't charge your card. Try again or contact our team for support.  
        🇷🇺 Упс, что-то пошло не так... Мы не смогли списать деньги с карты. Попробуйте заного или напишите в нашу службу поддержки и мы вам поможем разобраться. 
        """,
    )


@bot.message_handler(content_types=["successful_payment"])
def got_payment(message):
    bot.send_message(
        message.chat.id,
        """🇬🇧 Thank you for shopping with our PoLa Baker Store bot! Fetching products for your order # {}... 🛍  
        🇷🇺 Спасибо за покупку у нашего PoLa Baker Store бота! Сейчас доставим продукты по Вашему заказу № {}... 🛍""".format(
            message.successful_payment.provider_payment_charge_id,
            message.successful_payment.provider_payment_charge_id,
        ),
    )
    send_deliverables(bot, message, message.successful_payment.invoice_payload)


@bot.message_handler(func=lambda message: message.text == "📜 Terms / Условия")
def command_terms(message):
    # TODO: terms
    bot.send_message(message.chat.id, "📜 Terms & Conditions are currently being made.")


@bot.inline_handler(lambda query: len(query.query) == 0)
def query_all_products(inline_query):
    try:
        products = list_products()
        send_products(bot, inline_query, products, inline=True)
    except Exception as e:
        logger.exception(e)


bot.skip_pending = True

bot.polling()
