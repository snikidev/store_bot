import sentry_sdk
import os

SENTRY_DSN = os.environ['SENTRY_DSN']

sentry_sdk.init(SENTRY_DSN, traces_sample_rate=1.0)
