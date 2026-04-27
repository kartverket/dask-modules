import os
from databricks.sdk import WorkspaceClient
from rich.console import Console
from datacontract.data_contract import DataContract
from datacontract.output.test_results_writer import write_test_result
from pathlib import Path

console = Console()

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

changed_data_contracts = os.environ["CHANGED_DATA_CONTRACTS"]
changed_data_contracts_list_cleaned = [
    Path(file.strip())
    for file in (changed_data_contracts.split(",") if changed_data_contracts else [])
    if file.strip()
]

has_failed = False
for file in changed_data_contracts_list_cleaned:
    if file.suffix in [".yml", ".yaml"]:
        data_contract = DataContract(data_contract_file=str(file))
        run = data_contract.test()
        if not run.has_passed():
            has_failed = True
        write_test_result(
            run,
            console=console,
            output_format=None,
            output_path=None,
            data_contract=data_contract,
        )

if has_failed:
    raise Exception("Some data contracts failed tests. See logs for details.")
