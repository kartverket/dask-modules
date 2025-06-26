import json
import sys
from common import replace_special_characters

envs = ["dev", "prod"]

def should_keep_line(line: str) -> bool:
    lines_to_keep = ["databricks_workspace_url", "environment"]
    for line_to_keep in lines_to_keep:
        if line_to_keep in line:
            return True
    
    return False

def update_tfvar_file(monorepo_folder_path: str, env: str, project_name: str, project_id: str, project_number: str, area_name: str) -> None:
    tfvars_path = f'{monorepo_folder_path}/terraform/variables/{env}.tfvars'
    
    with open(tfvars_path) as file:
        lines = list(filter(should_keep_line, file.readlines()))
        file.close()

        lines.insert(0, f'repo_name = "{project_name.lower()}-data-ingestor"\n')
        lines.insert(0, f'landing_zone_bucket = "landing-zone-{project_id}"\n')
        lines.insert(0, f'compute_service_account = "databricks-compute@{project_id}.iam.gserviceaccount.com"\n')
        lines.insert(0, f'deploy_service_account = "{project_name.lower()}-deploy@{project_id}.iam.gserviceaccount.com"\n')
        lines.insert(0, f'project_number = "{project_number}"\n')
        lines.insert(0, f'project_id = "{project_id}"\n')
        lines.insert(0, f'area_name = "{area_name}"\n')
        lines.insert(0, f'team_name = "{project_name.lower()}"\n')

        with open(tfvars_path, 'w') as file:
            file.writelines(lines)
            file.close()


def update_state_bucket(monorepo_folder_path: str, env: str, val_for_env: str) -> None:
    with open(f'{monorepo_folder_path}/terraform/backend/{env}.gcs.tfbackend', 'w') as file:
        file.write(f'bucket = "{val_for_env}"\n')
        file.close()


def update_databricks_bundle_yml(file_path: str, area_name: str, project_name: str):
    config_path = f'{file_path}/databricks.yml'

    with open(config_path, 'r') as file:
        lines = [line.replace("plattform_dataprodukter", f"{area_name.lower()}_{project_name.lower()}") for line in file.readlines()]
        file.close()

        with open(config_path, 'w') as file:
            file.writelines(lines)
            file.close()


def clear_codeowners(file_path: str, team_name: str):
    codeowners_path = f'{file_path}/CODEOWNERS'
    
    with open(codeowners_path, 'r') as file:
        file_content = file.read()
        file_content = file_content.replace("Team DASK (Dataplattform Statens Kartverk)", f"Team {team_name}")
        file_content = file_content.replace("@kartverket/dask", f"@kartverket/{team_name}")
        file_content = file_content.replace("@sondrfos", "<<enter security champion (@username) here>>")
        file.close()

        with open(codeowners_path, 'w') as file:
            file.write(file_content)
            file.close()


def clear_catalog_info(file_path: str, team_name: str, project_name: str):
    cataloginfo_path = f'{file_path}/catalog-info.yaml'

    with open(cataloginfo_path, 'r') as file:
        file_content = file.read()
        file_content = file_content.replace("dask-monorepo-reference-setup", f'{project_name.lower()}-data-ingestor')
        file_content = file_content.replace("documentation", "dask jobs")
        file_content = file_content.replace("dataplattform", team_name)
        file.close()

        with open(cataloginfo_path, 'w') as file_out:
            file_out.write(file_content)
            file_out.close()


def configure_github_deploy_workflow(file_path: str, env: str, project_name: str, project_id: str, project_number: str):
    workflows_path = f'{file_path}/.github/workflows'

    deploy_sa_to_replace = {
        "dev": "dataplattform-deploy@dataprodukter-dev-5daa.iam.gserviceaccount.com",
        "prod": "dataplattform-deploy@dataprodukter-prod-d62f.iam.gserviceaccount.com"
    }
    copmute_sa_to_replace = {
        "dev": "databricks-compute@dataprodukter-dev-5daa.iam.gserviceaccount.com",
        "prod": "databricks-compute@dataprodukter-prod-d62f.iam.gserviceaccount.com"
    }
    project_number_to_replace = {
        "dev": "167289175624",
        "prod": "220770510673"
    }
    repo_to_replace = "dask-monorepo-reference-setup"
    project_name_to_replace = "dataprodukter"

    replacement_tuples = [
        (project_number_to_replace[env], project_number),
        (deploy_sa_to_replace[env], f'{project_name.lower()}-deploy@{project_id}.iam.gserviceaccount.com'),
        (copmute_sa_to_replace[env], f'{project_name.lower()}-deploy@{project_id}.iam.gserviceaccount.com'),
        (repo_to_replace, f'{project_name.lower()}-data-ingestor'),
        (project_name_to_replace, project_name.lower()),
    ]
    
    with open(f'{workflows_path}/deploy-{env}.yml') as file:
        lines = file.readlines()
        file.close()
        
        for replacement in replacement_tuples:
            lines = [line.replace(replacement[0], replacement[1]) for line in lines]
    
        with open(f'{workflows_path}/deploy-{env}.yml', 'w') as file:
            file.writelines(lines)
            file.close()


def edit_file(file_path, json_obj):
    team_name: str = json_obj.get("team_name")
    area_name: str = replace_special_characters(json_obj.get("area_name"))
    project_name: str = json_obj.get("project_name")

    clear_codeowners(file_path, team_name)
    update_databricks_bundle_yml(file_path, area_name, project_name)
    clear_catalog_info(file_path, team_name, project_name)

    for env in envs:
        state_bucket_for_env = json_obj.get("gcp_state_buckets")[env]
        update_state_bucket(file_path, env, state_bucket_for_env)

        project_id_for_env = json_obj.get("gcp_project_ids")[env]
        auth_project_number_for_env = json_obj.get("gcp_auth_numbers")[env]
        area_name = json_obj.get("area_name")
        update_tfvar_file(file_path, env, project_name, project_id_for_env, auth_project_number_for_env, area_name)

        configure_github_deploy_workflow(file_path, env, project_name, project_id_for_env, auth_project_number_for_env)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <file_path> <json_object>")
        sys.exit(1)

    file_path = sys.argv[1]
    json_str = sys.argv[2]
    json_obj = json.loads(json_str)

    edit_file(file_path, json_obj)

