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
    print(message)
    is_russian = message.from_user.language_code == "ru"

    terms_button_text = "📜 Условия" if is_russian else "📜 Terms"
    products_button_text = "🛍 Продукты" if is_russian else "🛍 Products"

    markup = ReplyKeyboardMarkup(row_width=1)
    terms_button = KeyboardButton(terms_button_text)
    products_button = KeyboardButton(products_button_text)
    markup.add(products_button, terms_button)

    message_text = (
        "Привет и добро пожаловать в PoLa Baker store bot!👋 Смотрите, что у нас в наличии! 🙌"
        if is_russian
        else "Hi, and welome to the PoLa Baker store bot!👋 Check out what we currently have on sale. Cheers! 🙌",
    )

    bot.send_message(
        message.chat.id,
        message_text,
        parse_mode="Markdown",
        reply_markup=markup,
    )


@bot.message_handler(
    func=lambda message: message.text == "🛍 Products" or message.text == "🛍 Продукты"
)
def handle_send_products(message):
    is_russian = message.from_user.language_code == "ru"
    try:
        products = list_products()
        send_products(bot, message, products)

    except Exception as e:
        logger.exception(e)
        error_message = (
            "Упс, что-то пошло не так... Попробуйте заного запросить продукты."
            if is_russian
            else "Oops, something went wrong... Try getting the products again."
        )
        bot.send_message(
            message.chat.id,
            error_message,
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
    is_russian = message.from_user.language_code == "ru"
    order_number = message.successful_payment.provider_payment_charge_id

    message_text = (
        f"Спасибо за покупку у нашего PoLa Baker Store бота! Сейчас доставим продукты по Вашему заказу №{order_number}... 🛍"
        if is_russian
        else f"Thank you for shopping with our PoLa Baker Store bot! Fetching products for your order #{order_number}... 🛍 "
    )
    print(message_text)
    bot.send_message(message.chat.id, message_text)
    send_deliverables(bot, message)


@bot.message_handler(
    func=lambda message: message.text == "📜 Условия" or message.text == "📜 Terms"
)
def command_terms(message):
    bot.send_message(
        message.chat.id,
        """📜 Terms & Conditions
        1. When you purchase access to the Digital Products you are purchasing a non-transferable, non-exclusive right to access the information. You may not publish or share the Digital Products with anyone else.
        2. Return, refund and cancellation policy: Due to the nature of the product, we cannot offer refunds on Digital Products. Should you consider your situation to be a special circumstance then please get in contact with us and we shall consider your invidual request. In the event that we do issue a refund, your access to the Digital Products will be revoked.
        3. PoLa Baker reserves all other rights.
        4. PoLa Baker provides no guarantee of availability of the web server or hosting of the Digital Products. We will make commercially reasonable efforts to provide availability.
        5. PoLa Baker reserves the right to vary these terms from time to time.
        """,
    )


@bot.inline_handler(lambda query: len(query.query) == 0)
def query_all_products(inline_query):
    try:
        products = list_products()
        send_products(bot, inline_query, products, inline=True)
    except Exception as e:
        logger.exception(e)


bot.skip_pending = True

bot.polling()
