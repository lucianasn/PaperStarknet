import json
import pandas as pd

from developers_info import coreDevelopers
from developers_info import statsDevelopers
from utils import constants as c
from utils import save_json as s

def main():
    repo_total_commits = get_all_developers()
    get_contributor_commits(repo_total_commits)

def get_all_developers():
    print("Getting info from all developers by repo ..")
    columns = ['id', 'full_name', 'login', 'email', 'commits_count', 'core_dev']
    s.create_empty_csv_file(c.colaborators_path, columns)

    repos_list = open(c.repositories_path, 'r', encoding='utf-8').readlines()        
    repo_total_commits = __save_contributors_by_repo(repos_list, columns)

    print("done.")
    return repo_total_commits

  


def get_contributor_commits(repo_total_commits):
    print("Detecting core developers ...")
    colaborators_data_df = pd.read_csv(c.colaborators_path)
   
    updated_colaborators_df = pd.DataFrame(columns=colaborators_data_df.columns)

    for repo in repo_total_commits:
        full_name = repo['full_name']
        column = colaborators_data_df['full_name']
        filtered_colaborators = colaborators_data_df[column == full_name]
        
        coreDevelopers.calculate_core_developers(filtered_colaborators, repo['total_commits'])
        updated_colaborators_df = pd.concat([updated_colaborators_df, filtered_colaborators], ignore_index=True)
        
    updated_colaborators_df.to_csv(c.colaborators_path, index=False)
    print("done.")
    

    
###################### Private Functions #################################

def __save_contributors_by_repo(repos_list, columns):
    repo_total_commits = []

    for repo in repos_list:
        repo = json.loads(repo)
        full_name = repo['full_name']
        
        query_info = {
            'id': repo['id'],
            'full_name': full_name, 
            'token': c.github_token,
            'url': f'{c.GITHUB_API_RV3}{full_name}',
            'contributors_url': repo['contributors_url']
        }
        
        print(f'Repo: {full_name}')
        (contributors_info, total_commits_repo) = coreDevelopers.get_all_contributors_repo(query_info)

        repo_commit = {
            'full_name': full_name,
            'total_commits': total_commits_repo
        }

        repo_total_commits.append(repo_commit)
    
        contributor_df = pd.DataFrame(contributors_info, columns=columns)
        coreDevelopers.sort_contributor_info_by_number_commits_df(contributor_df, columns[4])
        contributor_df.to_csv(c.colaborators_path, mode='a', index=False, header=False)

    return repo_total_commits
        
main()