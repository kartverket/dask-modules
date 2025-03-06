import json
import sys
from common import append_content_to_end_of_file, is_content_in_file


def generate_module_definition(project_name: str) -> str: 
    module = f'''
    module "{project_name.lower()}" {{
        source    = "./project_team"
        team_name = "{project_name}"
        repositories = [
            "kartverket/{project_name.lower()}-data-ingestor",
        ]
        extra_team_sa_roles = [
            "roles/resourcemanager.projectIamAdmin",
            "roles/iam.serviceAccountTokenCreator",
            "roles/iam.serviceAccountUser",
            "roles/secretmanager.admin",
            "roles/storage.admin",
            "roles/serviceusage.serviceUsageAdmin",
            "roles/cloudfunctions.admin",
            "roles/cloudscheduler.admin"
        ]
        env                   = var.env
        project_id            = var.{project_name}_project_id
        kubernetes_project_id = var.kubernetes_project_id
        can_manage_sa         = true
    }}
    '''

    return module


def edit_file(file_path, params):
    project_name: str = params.get("project_name")
    project_ids = params["gcp_project_ids"]
    project_id_sandbox = project_ids["sandbox"]
    project_id_dev = project_ids["dev"]
    project_id_prod = project_ids["prod"]

    # Handle modules.tf
    module_definition = generate_module_definition(project_name)
    append_content_to_end_of_file(file_path + "/modules.tf", module_definition)

    # Handle variables.tf
    variable_def = f'variable "{project_name}_project_id" {{}}\n'
    if not is_content_in_file(file_path + "/variables.tf", variable_def):
        append_content_to_end_of_file(file_path + "/variables.tf", variable_def)

    # Handle *.tfvars files
    get_project_var_entry = lambda project: f'\n{project_name}_project_id = "{project}"'
    
    sandbox_var_entry = get_project_var_entry(project_id_sandbox)
    if not is_content_in_file(file_path + "/sandbox.tfvars", sandbox_var_entry):
        append_content_to_end_of_file(file_path + "/sandbox.tfvars", sandbox_var_entry)

    dev_var_entry = get_project_var_entry(project_id_dev)
    if not is_content_in_file(file_path + "/dev.tfvars", dev_var_entry):
        append_content_to_end_of_file(file_path + "/dev.tfvars", dev_var_entry)

    prod_var_entry = get_project_var_entry(project_id_prod)
    if not is_content_in_file(file_path + "/prod.tfvars", prod_var_entry):
        append_content_to_end_of_file(file_path + "/prod.tfvars", prod_var_entry)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <file_path> <json_object>")
        sys.exit(1)

    file_path = sys.argv[1]
    json_str = sys.argv[2]
    params = json.loads(json_str)

    edit_file(file_path, params)

# python gcp_service_accounts.py './path/to/gcp_service_accounts' '{ "project_name": "testteam", "gcp_project_ids": { "sandbox": "project-sandbox", "dev": "project-dev", "prod": "project-prod" } }'
