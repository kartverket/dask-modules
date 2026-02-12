import os
from databricks.sdk import WorkspaceClient
from datacontract.data_contract import DataContract
from pathlib import Path

if os.environ["ENVIRONMENT"] == "dev":
    os.environ["DATACONTRACT_DATABRICKS_SERVER_HOSTNAME"] = (
        "https://2004011444667850.0.gcp.databricks.com"
    )
    os.environ["DATACONTRACT_DATABRICKS_HTTP_PATH"] = (
        "/sql/1.0/warehouses/43ebd38bb3fbe7ac"
    )
elif os.environ["ENVIRONMENT"] == "prod":
    os.environ["DATACONTRACT_DATABRICKS_SERVER_HOSTNAME"] = (
        "https://3359340685875444.4.gcp.databricks.com"
    )
    os.environ["DATACONTRACT_DATABRICKS_HTTP_PATH"] = (
        "/sql/1.0/warehouses/7b7b34fd5e55d6f1"
    )
else:
    raise ValueError("Invalid environment. Must be 'dev' or 'prod'.")


ws_client = WorkspaceClient(
    host=os.environ["DATACONTRACT_DATABRICKS_SERVER_HOSTNAME"],
    google_service_account=os.environ["SERVICE_ACCOUNT"],
)

os.environ["DATACONTRACT_DATABRICKS_TOKEN"] = str(
    ws_client.api_client._cfg.oauth_token()
)

changed_datacontracts = os.environ["CHANGED_DATACONTRACTS"]
print(f"Changed data contracts: {changed_datacontracts}")

changed_datacontracts_list = (
    changed_datacontracts.split(",") if changed_datacontracts else []
)
changed_datacontracts_list_cleaned = [
    file.strip() for file in changed_datacontracts_list if file.strip()
]


has_failed = False
for file in changed_datacontracts_list_cleaned:
    if file.endswith(".yml") or file.endswith(".yaml"):
        data_contract = DataContract(data_contract_file=file)
        run = data_contract.test()
        if not run.has_passed():
            has_failed = True
            print(f"Data contract {file} failed tests:")
            print(run.pretty_logs())

if has_failed:
    raise Exception("Some data contracts failed tests. See logs for details.")
