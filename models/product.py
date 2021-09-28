from pydantic import BaseModel, Field, root_validator
from common.settings import Settings
from telegram import LabeledPrice

settings = Settings()


class Product(BaseModel):
    currency: str = "gbp"
    description: str
    title: str
    payload: str = Field(alias="id")
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

    @root_validator(pre=True)
    def get_nested_values(cls, values):
        title, price, thumbnail_large = (
            values.get("title"),
            values.get("price"),
            values.get("photo")[0].get("thumbnails").get("large"),
        )

        photo_url = thumbnail_large.get("url").replace(" ", "%20")
        photo_height = thumbnail_large.get("height")
        photo_width = thumbnail_large.get("width")

        prices = [
            LabeledPrice(
                label=str(title),
                amount=int(price * 100),
            )
        ]

        return dict(
            values,
            photo_url=photo_url,
            prices=prices,
            photo_height=photo_height,
            photo_width=photo_width,
        )
