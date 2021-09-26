from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    airtable_api_key: str
    airtable_base_id: str
    bot_token: str
    python_env: str
    sentry_dsn: str
    stripe_api_key: str
    stripe_token: str
    airtable_api_url: str = ""

    @root_validator(pre=False)
    def _set_fields(cls, values):
        airtable_api_url = "https://api.airtable.com/v0/{}/Products".format(
            values["airtable_base_id"]
        )

        return dict(values, airtable_api_url=airtable_api_url)
