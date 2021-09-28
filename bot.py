from dotenv import load_dotenv

load_dotenv()

import common.sentry
from common.settings import Settings
from common.dictionary import dictionary
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    PreCheckoutQueryHandler,
    InlineQueryHandler,
)
from handlers import (
    start,
    products,
    terms,
    successful_payment,
    pre_checkout,
    inline_query,
)


def main() -> None:
    settings = Settings()
    updater = Updater(settings.bot_token)
    dispatcher = updater.dispatcher

    # Simple start function
    dispatcher.add_handler(CommandHandler("start", start.start))

    # Products handler
    dispatcher.add_handler(
        MessageHandler(
            Filters.regex(f'^{dictionary["en"].products}$'), products.products_handler
        )
    )
    dispatcher.add_handler(
        MessageHandler(
            Filters.regex(f'^{dictionary["ru"].products}$'), products.products_handler
        )
    )

    # Terms & Conditions handler
    dispatcher.add_handler(
        MessageHandler(
            Filters.regex(f'^{dictionary["ru"].terms_and_conditions}$'), terms.terms
        )
    )
    dispatcher.add_handler(
        MessageHandler(
            Filters.regex(f'^{dictionary["en"].terms_and_conditions}$'), terms.terms
        )
    )

    # Inline query handler
    dispatcher.add_handler(InlineQueryHandler(inline_query.inline_query))

    # Pre-checkout handler to final check
    dispatcher.add_handler(PreCheckoutQueryHandler(pre_checkout.pre_checkout))

    # Success! Notify your user!
    dispatcher.add_handler(
        MessageHandler(
            Filters.successful_payment, successful_payment.successful_payment
        )
    )

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
