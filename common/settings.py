from pydantic import BaseSettings


class Settings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    bot_token: str
    commercejs_token: str
    python_env: str
    sentry_dsn: str
    stripe_api_key: str
    stripe_token: str
    s3_bucket_name: str
