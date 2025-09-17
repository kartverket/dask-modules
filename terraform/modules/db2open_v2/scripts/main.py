from databricks.sdk import WorkspaceClient
import os
import datetime
import json
import requests
from urllib.parse import urlparse
from google.cloud import storage

days = float(os.environ.get("DAYS", "1"))
hours = float(os.environ.get("HOURS", "0"))
minutes = float(os.environ.get("MINUTES", "0"))
seconds = float(os.environ.get("SECONDS", "0"))

def _build_activation_url(databricks_host: str, activation_token: str) -> str:
    """
    Build the public activation endpoint URL from the configured workspace host.
    """
    parsed = urlparse(databricks_host if databricks_host.startswith("http") else f"https://{databricks_host}")
    base = f"{parsed.scheme}://{parsed.netloc}"
    return f"{base}/api/2.1/unity-catalog/public/data_sharing_activation/{activation_token}"

def main(request):
    print("os.environ")
    print(os.environ)
    delta_share_name = os.environ.get("DELTA_SHARE_NAME")
    delta_recipient_name = os.environ.get("DELTA_RECIPIENT_NAME")
    databricks_host = os.environ.get("DATABRICKS_HOST")
    bucket_name = os.environ.get("BUCKET_NAME")
    config_file_name = os.environ.get("CONFIG_FILE_NAME", "config.share") 

    if delta_share_name is None:
        raise ValueError("Env variable DELTA_SHARE_NAME is required")
    
    if delta_recipient_name is None:
        raise ValueError("Env variable DELTA_RECIPIENT_NAME is required")

    expiration_datetime = datetime.datetime.now() + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    expiration_timestamp_ms = int(expiration_datetime.timestamp() * 1000)

    ws_client = WorkspaceClient(
        host=databricks_host,
        google_service_account=os.environ["DATABRICKS_GOOGLE_SERVICE_ACCOUNT"]
    )

    rotated_token = ws_client.recipients.rotate_token(delta_recipient_name, existing_token_expire_in_seconds=0)
    ws_client.recipients.update(delta_recipient_name, expiration_time=expiration_timestamp_ms)

    if len(rotated_token.tokens) != 1:
        print("No tokens found or too many tokens found")
        print(rotated_token.tokens)
        raise Exception("No tokens found or too many tokens found")

    activation_token = rotated_token.tokens[0].activation_url.split("?")[-1]

    bucket_name = os.environ["BUCKET_NAME"]

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    activation_endpoint = _build_activation_url(databricks_host, activation_token)
    resp = requests.get(activation_endpoint, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to fetch share config (HTTP {resp.status_code}): {resp.text}")

    sharing_data = resp.json()

    share_config = {
        "shareCredentialsVersion": sharing_data.get("shareCredentialsVersion"),
        "bearerToken": sharing_data.get("bearerToken"),
        "endpoint": sharing_data.get("endpoint"),
        "expirationTime": sharing_data.get("expirationTime"),
    }

    missing = [k for k in ("shareCredentialsVersion", "bearerToken", "endpoint") if not share_config.get(k)]
    if missing:
        raise RuntimeError(f"Activation response missing keys: {missing}. Raw: {sharing_data}")

    config_blob = bucket.blob(config_file_name)

    config_blob.upload_from_string(json.dumps(share_config, indent=2), content_type="application/json")

    print(f"Delta Sharing config written to gs://{bucket_name}/{config_file_name}")
    return "OK"

if __name__ == "__main__":
    main()