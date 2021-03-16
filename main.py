import os
import datetime

from flask import escape
from google.cloud import storage
from google.oauth2 import service_account

import environ

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# check if .env file exists
env_file = os.path.join(BASE_DIR, ".env")
# If no .env has been provided, pull it from Secret Manager
if os.path.isfile(env_file):
    env = environ.Env()
    env.read_env(env_file)

storage_client = None
if os.getenv("APP_ENV", None) == "LOCAL":
    GOOGLE_APPLICATION_CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.path.join(BASE_DIR, env("GOOGLE_APPLICATION_CREDENTIALS_FILE"))
    )
    storage_client = storage.Client(
        credentials=GOOGLE_APPLICATION_CREDENTIALS
    )
else:
    storage_client = storage.Client()


def copy_blob(request=None):
    """Copies a blob from one bucket to another with a new name."""
    time = datetime.datetime.now().strftime("%H%M%S")
    bucket_name = os.getenv("SOURCE_BUCKET")
    blob_name = os.getenv("SOURCE_BLOB_NAME")
    destination_bucket_name = os.getenv("TARGET_BUCKET")
    destination_blob_name = os.getenv("TAGET_BLOB_NAME")+time
  
    # storage_client = storage.Client()

    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name
    )

    print(
        "Blob {} in bucket {} copied to blob {} in bucket {}.".format(
            source_blob.name,
            source_bucket.name,
            blob_copy.name,
            destination_bucket.name,
        )
    )

if __name__ == "__main__":
    copy_blob(None)
