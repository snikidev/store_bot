from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from common.get_deliverables import get_deliverables
from common.dictionary import dictionary


def send_deliverables(update: Update, context: CallbackContext):
    language_code, invoice_payload = (
        update.message.from_user.language_code,
        update.message.successful_payment.invoice_payload,
    )

    deliverables = get_deliverables(invoice_payload)

    for index, obj in enumerate(deliverables):
        url = obj.get("url")
        message_text = dictionary[language_code].deliverable_message.format(
            index + 1, len(deliverables), url
        )

        context.bot.send_message(update.message.chat.id, message_text, parse_mode=ParseMode.MARKDOWN,)
