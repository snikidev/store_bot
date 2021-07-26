import telebot
from dotenv import load_dotenv
load_dotenv()
# TODO: import common.sentry
from telebot.types import LabeledPrice
from common.list_products import list_products
from common.send_products import send_products
from common.get_deliverables import get_deliverables
from common.settings import Settings

settings = Settings()
bot = telebot.TeleBot(settings.bot_token, parse_mode=None)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    try:
        products = list_products()
        bot.send_message(message.chat.id,
                         # TODO: welcome message
                         'Hi, and welome to the store!👋 Check out what we currently have on sale, and let us know if you don\'t find anything you like, or have any other feedback by typing /feedback. Cheers! 🙌',
                         parse_mode='Markdown')
        send_products(bot, message, products)
    except:
        bot.send_message(
            message.chat.id, 'Oops, something went wrong... Try getting products again by typing /products')


@bot.message_handler(commands=["products"])
def handle_send_products(message):
    # try:
    products = list_products()
    send_products(bot, message, products)
    # except:
    #     bot.send_message(
    #         message.chat.id, 'Oops, something went wrong... Try getting products again by typing /products')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Oops, something went wrong... We couldn't charge your card. Try again or contact our team for support.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    deliverables = get_deliverables(message.successful_payment.invoice_payload)
    bot.send_message(message.chat.id, 'Hoooooray!')


@bot.message_handler(commands=['terms'])
def command_terms(message):
    # TODO: send file on successful purchase here
    # TODO: list orderID number here
    bot.send_message(message.chat.id,
                     'Thank you for shopping with our PoLa Baker Store bot! Please, find your product below.🛍')


bot.skip_pending = True


bot.polling()
