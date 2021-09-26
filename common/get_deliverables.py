import requests
from common.settings import Settings

settings = Settings()


def get_deliverables(invoice_payload):
    url = (
        settings.airtable_api_url
        + f"/{invoice_payload}"
        + f"?api_key={settings.airtable_api_key}"
    )

    product = requests.request("GET", url).json()

    return product["fields"]["files"]
