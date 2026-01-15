import json
import sys
import textwrap
from typing import List


def is_content_in_file(file_path: str, content: str) -> bool:
    with open(file_path) as file:
        file_content = file.read()
        return file_content.find(content) > -1


def append_content_to_end_of_file(file_path: str, content: str) -> None:
    lines: List[str] = []
    with open(file_path) as file:
        lines = file.readlines()

    if lines and not lines[-1].endswith('\n'):
        lines[-1] += '\n'

    lines.append(textwrap.dedent(content) + '\n')

    with open(file_path, 'w') as file:
        file.writelines(lines)


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


def edit_file(file_path, params: dict):
    division: str = params.get("area_name")
    team: str = params.get("project_name")

    module_content = generate_checks_per_team_module(division, team)

    # Sjekk om teamet allerede finnes
    identifier = f'checks_per_team_{team}'
    if not is_content_in_file(file_path + "/databricks.tf", identifier):
        append_content_to_end_of_file(file_path + "/databricks.tf", module_content)
    else:
        print(f"Module checks_per_team_{team} already exists in databricks.tf. Skipping append.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Mangler argumenter")
        sys.exit(1)

    file_path = sys.argv[1]
    json_str = sys.argv[2]
    params = json.loads(json_str)

    edit_file(file_path, params)
