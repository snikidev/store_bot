from pydantic import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    stripe_token: str
    stripe_api_key: str
    commercejs_token: str
    sentry_dsn: str
    python_env: str
    firebase_project: str
