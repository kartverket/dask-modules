import json
import sys
from common import append_content_to_end_of_file, is_content_in_file


def generate_checks_per_team_module(division: str, team: str) -> str:
    return f'''
module "checks_per_team_{team}" {{
  source               = "./modules/checks-per-team"
  cluster_policy_id    = var.cluster_policy_id
  slack_integration_id = var.slack_integration_id
  base_repo_path       = databricks_permissions.run_permission_on_dask_governance.directory_path
  environment          = var.environment
  division             = "{division}"
  team                 = "{team}"
  compute_sa_users     = local.compute_sa_users
}}
'''


def edit_file(file_path, params):
    division: str = params.get("division")
    team: str = params.get("team")

    module_content = generate_checks_per_team_module(division, team)

    # Sjekk om teamet allerede finnes
    identifier = f'checks_per_team_{team}'
    if not is_content_in_file(file_path + "/modules.tf", identifier):
        append_content_to_end_of_file(file_path + "/modules.tf", module_content)
    else:
        print(f"Module checks_per_team_{team} already exists in modules.tf. Skipping append.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Mangler argumenter")
        sys.exit(1)

    file_path = sys.argv[1]
    json_str = sys.argv[2]
    params = json.loads(json_str)

    edit_file(file_path, params)