from google.cloud import storage
from google.oauth2 import service_account
from common.settings import Settings

settings = Settings()

secret_path = "~/etc/secrets/firebaseToken.json" if settings.python_env == "production" else "./firebaseToken.json"

credentials = service_account.Credentials.from_service_account_file(
    secret_path)
client = storage.Client(credentials=credentials,
                        project=settings.firebase_project)
bucket = storage.Bucket(client, settings.firebase_project,
                        user_project=settings.firebase_project)

# TODO: this doesn't work, I think
def get_deliverables(folder):
    deliverables = list(client.list_blobs(bucket + "/" + folder))
    return deliverables
