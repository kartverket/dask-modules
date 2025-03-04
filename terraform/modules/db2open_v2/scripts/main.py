from databricks.sdk import WorkspaceClient
import os
import datetime
import json
from google.cloud import storage

days = float(os.environ.get("DAYS", "1"))
hours = float(os.environ.get("HOURS", "0"))
minutes = float(os.environ.get("MINUTES", "0"))
seconds = float(os.environ.get("SECONDS", "0"))

def main(request):
    print("os.environ")
    print(os.environ)
    delta_share_name = os.environ.get("DELTA_SHARE_NAME", None)
    delta_recipient_name = os.environ.get("DELTA_RECIPIENT_NAME", None)

    if delta_share_name is None:
        raise ValueError("Env variable DELTA_SHARE_NAME is required")
    
    if delta_recipient_name is None:
        raise ValueError("Env variable DELTA_RECIPIENT_NAME is required")

    expiration_datetime = datetime.datetime.now() + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    expiration_timestamp_ms = int(expiration_datetime.timestamp() * 1000)

    ws_client = WorkspaceClient(
        host=os.environ["DATABRICKS_HOST"],
        google_service_account=os.environ["DATABRICKS_GOOGLE_SERVICE_ACCOUNT"]
    )

    rotated_token = ws_client.recipients.rotate_token(delta_recipient_name, existing_token_expire_in_seconds=0)
    ws_client.recipients.update(delta_recipient_name, expiration_time=expiration_timestamp_ms)

    if len(rotated_token.tokens) != 1:
        print("No tokens found or too many tokens found")
        print(rotated_token.tokens)
        raise Exception("No tokens found or too many tokens found")

    activation_token = rotated_token.tokens[0].activation_url.split("?")[-1]
    file_content = { "activation_token": activation_token, "expiration_time": expiration_datetime.isoformat() }


    bucket_name = os.environ["BUCKET_NAME"]
    file_name = os.environ["TOKEN_FILE_NAME"]

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_string(json.dumps(file_content))

    print(f"Activation token written to gs://{bucket_name}/{file_name}")

    return 'OK'

if __name__ == "__main__":
    main()