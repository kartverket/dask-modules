import os
from databricks.sdk import WorkspaceClient
from datacontract.data_contract import DataContract

if os.environ["ENVIRONMENT"] == "dev":
    os.environ["DATACONTRACT_DATABRICKS_SERVER_HOSTNAME"] = (
        "https://2004011444667850.0.gcp.databricks.com"
    )
    os.environ["DATACONTRACT_DATABRICKS_HTTP_PATH"] = (
        "/sql/1.0/warehouses/822bdad63909bcd2"
    )
elif os.environ["ENVIRONMENT"] == "prod":
    os.environ["DATACONTRACT_DATABRICKS_SERVER_HOSTNAME"] = (
        "https://2004011444667850.0.gcp.databricks.com"
    )
    os.environ["DATACONTRACT_DATABRICKS_HTTP_PATH"] = (
        "/sql/1.0/warehouses/822bdad63909bcd2"
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

datacontract_path = os.environ["DATACONTRACT_PATH"]
has_failed = False
for file in os.listdir(datacontract_path):
    if file.endswith(".yml") or file.endswith(".yaml"):
        data_contract = DataContract(
            data_contract_file=os.path.join(datacontract_path, file)
        )
        run = data_contract.test()
        if not run.has_passed():
            has_failed = True
            print(f"Data contract {file} failed tests:")
            print(run.pretty_logs())

if has_failed:
    raise Exception("Some data contracts failed tests. See logs for details.")
