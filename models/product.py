from pydantic import BaseModel, Field, root_validator
from common.settings import Settings
from telebot.types import LabeledPrice
from helpers.formatters import html_to_string_formatter

settings = Settings()


class Product(BaseModel):
    currency: str = "gbp"
    description: str
    invoice_payload: str = Field(alias="id")
    is_flexible: bool = False  # True If you need to set up Shipping Fee
    need_email: bool = True
    photo_height: int = 512  # !=0/None or picture won't be shown
    photo_size: int = 512
    photo_url: str = None
    photo_width: int = 1000
    prices: list = []
    provider_token: str = settings.stripe_token
    send_email_to_provider: bool = True
    start_parameter: str = Field(alias="id")
    title: str = Field(alias="name")

    @root_validator(pre=True)
    def get_nested_values(cls, values):
        photo_url = values.get("media").get("source").replace(" ", "%20")
        prices = [
            LabeledPrice(
                label=str(values.get("name")),
                amount=int(values.get("price").get("raw") * 100),
            )
        ]
        description = html_to_string_formatter(values.get("description"))

        return dict(values, photo_url=photo_url, prices=prices, description=description)
