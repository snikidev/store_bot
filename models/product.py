from pydantic import BaseModel, Field, root_validator
from common.settings import Settings
from telebot.types import LabeledPrice
from helpers.formatters import html_to_string_formatter

settings = Settings()


class Product(BaseModel):
    title: str = Field(alias="name")
    description: str
    provider_token: str = settings.stripe_token
    start_parameter: str = Field(alias="id")
    invoice_payload: str = Field(alias="id")
    is_flexible: bool = False  # True If you need to set up Shipping Fee
    photo_height: int = 512  # !=0/None or picture won't be shown
    photo_width: int = 1000
    photo_size: int = 512
    currency: str = "gbp"
    prices: list = []
    photo_url: str = None

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
