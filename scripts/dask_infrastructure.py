import sys
import json

from common import replace_special_characters, append_content_to_end_of_file

TF_FOLDERS = {"dev": "dev", "prod": "prod_v2"}


def edit_common_output_file(filepath: str, params: dict):
    tf_output_file_path: str = f'{filepath}/modules_v2/common/output.tf'
    project_name: str = params.get("project_name")

    content = f'''
    output "{project_name.lower()}" {{
      value = local.{project_name.lower()}
    }}'''

    append_content_to_end_of_file(tf_output_file_path, content)


def edit_ws_configure_file(filepath: str, params: dict):
    project_name: str = params.get("project_name")

    project_id_map: dict = params["gcp_project_ids"]

    for env, tf_folder in TF_FOLDERS.items():
        tf_ws_configure_filepath = f'{filepath}/{tf_folder}/4_workspace_configure.tf'
        # Define the new team data
        new_team_data = generate_module_definition(project_name, project_id_map, env)

        append_content_to_end_of_file(tf_ws_configure_filepath, new_team_data)


def generate_module_definition(project_name: str, project_id_map: dict, env: str) -> str:
    module = f'''
    module "{project_name.lower()}" {{
      source = "../modules_v2/dbx_team_resources"

      team                    = module.common.{project_name.lower()}
      team_deploy_sa          = "{project_name.lower()}-deploy@{project_id_map[env]}.iam.gserviceaccount.com"
      project_id              = "{project_id_map[env]}"
      common_users_and_groups = local.common_users_and_groups
      config                  = local.config
    
      providers = {{
        databricks.accounts   = databricks.accounts
        databricks.workspace  = databricks.workspace
        google.global_storage = google.global_storage
      }}
    }}'''

    return module


def edit_common_teams_file(filepath: str, params: dict):
    tf_teams_file_path: str = f'{filepath}/modules_v2/common/teams.tf'
    ad_group_name: str = params["ad_groups"][0]
    project_name: str = params.get("project_name")
    area_name: str = params["area_name"]
    area_special_chars_replaced = replace_special_characters(area_name)

    team_content = f'''
    {project_name.lower()} = {{
      ad_group_name = "AAD - TF - TEAM - {ad_group_name}"
      team_name     = "{project_name.lower()}"
      area_name     = "{area_special_chars_replaced.lower()}"
    }}
    '''

    with open(tf_teams_file_path, 'r') as file:
        content = file.read()

    index = content.rindex("}\n")

    new_content = ''.join([content[:index], team_content, content[index:]])

    with open(tf_teams_file_path, 'w') as file:
        file.write(new_content)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <file_path> <json_object>")
        sys.exit(1)

    file_path = sys.argv[1]
    json_str = sys.argv[2]
    params = json.loads(json_str)

    edit_ws_configure_file(file_path, params)
    edit_common_output_file(file_path, params)
    edit_common_teams_file(file_path, params)
