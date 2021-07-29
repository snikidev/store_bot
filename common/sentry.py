import sentry_sdk
from common.settings import Settings

settings = Settings()


sentry_sdk.init(settings.sentry_dsn, traces_sample_rate=1.0,
                environment=settings.python_env)
