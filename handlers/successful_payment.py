from telegram import Update
from telegram.ext import CallbackContext
from common.send_deliverables import send_deliverables
from common.dictionary import dictionary


def successful_payment(update: Update, context: CallbackContext) -> None:
    language_code = update.effective_user.language_code
    chat_id = update.message.chat_id
    order_number = update.message.successful_payment.provider_payment_charge_id
    message_text = dictionary[language_code].success_message.format(order_number)

    context.bot.send_message(chat_id, message_text)
    send_deliverables(update, context)