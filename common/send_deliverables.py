from common.get_deliverables import get_deliverables
from common.dictionary import dictionary


def send_deliverables(bot, message):
    language_code, invoice_payload = (
        message.from_user.language_code,
        message.successful_payment.invoice_payload,
    )

    deliverables = get_deliverables(invoice_payload)

    for index, obj in enumerate(deliverables):
        url = obj.get("url")
        message_text = dictionary[language_code].deliverable_message.format(
            index + 1, len(deliverables), url
        )

        bot.send_message(message.chat.id, message_text)
