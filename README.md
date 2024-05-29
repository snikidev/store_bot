# Telegram StoreBot

> Easy way to sell your digital goods online

A Telegram chat bot that users can interact with to browse, share and buy your products.

## Getting started
[] Create a bot in Telegram, following the [documentation](https://core.telegram.org/bots/payments)
[] Get [Airtable](https://airtable.com/)
[] [Optional] Get [Sentry](https://sentry.io/), in case you'd like to track errors and users' feedback for any potential improvements.
[] Personalise messages in `locales/en.py` and `locales/ru.py` to your liking.
| key                          | Note    |
| ---------------------        | ------- |
| `terms_and_conditions`         | Button text    |
| `products`                     | Button text     |
| `start_message`                | First message your users see when the send /start command    |
| `get_products_error`           | Message your users receive when there is a technical error when fetching products    |
| `terms_and_conditions_text`    | Terms and conditions of your purchase   |
| `success_message`              | Message showed on successful purchase while fetching `deliverable_message`     |
| `deliverable_message`          | Message with links to your product after payment has been successful    |
[] [Optional] Create more files in the `locales` folder if you need to support more languages.
[] Upload all products to Airtable, following [the template](https://airtable.com/appxjoyvxXZNl5prE/shrNYxolmgHYYwkU2/tblmNshp6ZIKyEUyG)
[] Check out `.env.example` for the necessary environment variables.
[] Deploy the bot and run it with `python3 bot.py`

## Contributing
Always welcome! Feel free to open an issue or a pull request.
