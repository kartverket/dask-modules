import argparse
import json
import re


def replace_special_characters(s):
    replacements = {
        'æ': 'ae',
        'Æ': 'Ae',
        'ø': 'o',
        'Ø': 'O',
        'å': 'aa',
        'Å': 'Aa'
    }

    return re.sub(r'[æåÆØÅ]', lambda match: replacements[match.group(0)], s)


envs = ["dev", "prod"]


def should_keep_line(line: str) -> bool:
    lines_to_keep = ["databricks_workspace_url", "environment"]
    for line_to_keep in lines_to_keep:
        if line_to_keep in line:
            return True

    return False


def replace_text_in_file(file_path: str, replacements: list[tuple[str, str]]) -> None:
    with open(file_path, "r") as file:
        content = file.read()
        for replace, replacement in replacements:
            content = content.replace(replace, replacement)

    with open(file_path, "w") as file:
        file.write(content)


def update_repo_name(resource_name: str) -> None:
    files = [
        "terraform/variables.tf",
        "databricks.yml"
    ]

    for change_file in files:
        replace_text_in_file(
            change_file,
            [("dask-monorepo-reference-setup", f"{resource_name}-data-ingestor")],
        )


def update_tfvar_file(
        env: str,
        resource_name: str,
        project_id: str,
        project_number: str,
        division: str,
) -> None:
    tfvars_path = f'terraform/variables/{env}.tfvars'

    with open(tfvars_path) as file:
        lines = list(filter(should_keep_line, file.readlines()))
        file.close()

        lines.insert(0, f'repo_name = "{resource_name}-data-ingestor"\n')
        lines.insert(0, f'landing_zone_bucket = "landing-zone-{project_id}"\n')
        lines.insert(0, f'compute_service_account = "databricks-compute@{project_id}.iam.gserviceaccount.com"\n')
        lines.insert(0,
                     f'deploy_service_account = "{resource_name}-deploy@{project_id}.iam.gserviceaccount.com"\n')
        lines.insert(0, f'project_number = "{project_number}"\n')
        lines.insert(0, f'project_id = "{project_id}"\n')
        lines.insert(0, f'area_name = "{division}"\n')
        lines.insert(0, f'team_name = "{resource_name}"\n')

        with open(tfvars_path, 'w') as file:
            file.writelines(lines)
            file.close()


def update_state_bucket(env: str, val_for_env: str) -> None:
    with open(f'terraform/backend/{env}.gcs.tfbackend', 'w') as file:
        file.write(f'bucket = "{val_for_env}"\n')
        file.close()


def update_databricks_bundle_yml(division: str, resource_name: str):
    config_path = 'databricks.yml'

    with open(config_path, 'r') as file:
        lines = [line.replace("plattform_dataprodukter", f"{division}_{resource_name}") for line in
                 file.readlines()]
        file.close()

        with open(config_path, 'w') as file:
            file.writelines(lines)
            file.close()


def update_codeowners(team_name: str, github_team: str):
    codeowners_path = 'CODEOWNERS'

    with open(codeowners_path, 'r') as file:
        file_content = file.read()
        file_content = file_content.replace("Team DASK (Dataplattform Statens Kartverk)", f"Team {team_name}")
        file_content = file_content.replace("@kartverket/dask", f"@kartverket/{github_team}")
        file_content = file_content.replace("@sondrfos", "<<enter security champion (@username) here>>")
        file.close()

        with open(codeowners_path, 'w') as file:
            file.write(file_content)
            file.close()


def update_catalog_info(resource_name: str):
    cataloginfo_path = 'catalog-info.yaml'

    with open(cataloginfo_path, 'r') as file:
        file_content = file.read()
        file_content = file_content.replace("dask-monorepo-reference-setup", f'{resource_name}-data-ingestor')
        file_content = file_content.replace("documentation", "ops")
        file_content = file_content.replace("dataplattform", resource_name)
        file.close()

        with open(cataloginfo_path, 'w') as file_out:
            file_out.write(file_content)
            file_out.close()


def configure_github_deploy_workflow(env: str, resource_name: str, project_id: str, project_number: str):
    workflows_path = '.github/workflows'

    deploy_sa_to_replace = {
        "dev": "dataplattform-deploy@dataprodukter-dev-5daa.iam.gserviceaccount.com",
        "prod": "dataplattform-deploy@dataprodukter-prod-d62f.iam.gserviceaccount.com"
    }
    compute_sa_to_replace = {
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
        (deploy_sa_to_replace[env], f'{resource_name}-deploy@{project_id}.iam.gserviceaccount.com'),
        (compute_sa_to_replace[env], f'databricks-compute@{project_id}.iam.gserviceaccount.com'),
        (repo_to_replace, f'{resource_name}-data-ingestor'),
        (project_name_to_replace, resource_name),
    ]

    with open(f'{workflows_path}/deploy-{env}.yml') as file:
        lines = file.readlines()
        file.close()

        for replacement in replacement_tuples:
            lines = [line.replace(replacement[0], replacement[1]) for line in lines]

        with open(f'{workflows_path}/deploy-{env}.yml', 'w') as file:
            file.writelines(lines)
            file.close()


def edit_file(json_obj: dict):
    resource_name: str = json_obj.get("resource_name")
    team_name: str = json_obj.get("team_name")
    github_team: str = json_obj.get("github_team")
    division: str = replace_special_characters(json_obj.get("division"))

    update_codeowners(team_name, github_team)
    update_databricks_bundle_yml(division, resource_name)
    update_catalog_info(resource_name)

    for env in envs:
        state_bucket_for_env = json_obj.get("gcp_state_buckets")[env]
        update_state_bucket(env, state_bucket_for_env)

        project_id_for_env = json_obj.get("gcp_project_ids")[env]
        project_number_for_env = json_obj.get("gcp_project_numbers")[env]
        update_tfvar_file(env, resource_name, project_id_for_env, project_number_for_env, division)
        update_repo_name(resource_name)

        configure_github_deploy_workflow(env, resource_name, project_id_for_env, project_number_for_env)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sett opp data-ingestor-repo for et nytt produktteam')
    payload_format = """
    {
        "team_name": string,
        "resource_name": string,
        "division": string,
        "github_team": string,
        "gcp_project_ids": {
            "sandbox": string,
            "dev": string,
            "prod": string
        },
        "gcp_project_numbers": {
            "sandbox": string,
            "dev": string,
            "prod": string
        },
        "gcp_state_buckets": {
            "sandbox": string,
            "dev": string,
            "prod": string
        }
    }
    """
    parser.add_argument('--payload', required=True, help=payload_format)

    args = parser.parse_args()
    params = json.loads(args.payload)

    edit_file(params)
