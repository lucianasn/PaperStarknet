import requests
import json
import pandas as pd

from datetime import datetime

from utils import constants as c
from utils import utilities as u
from utils import save_json as s

def main():
    print("Getting full history ...")
    get_all_commits()


def get_all_commits():
    repos_list = open(c.repositories_path, 'r', encoding='utf-8').readlines()  
    json_file = open(c.commits_path, 'w', encoding='utf-8')

    columns = ['id', 'full_name', 'commits']
    s.create_empty_csv_file(c.commits_path, columns)
    commits_repos = []

    for repo in repos_list:
        repo = json.loads(repo)
        full_name = repo['full_name']

        commits_url = f'{c.GITHUB_API_RV3}{full_name}/commits'
        headers = u.get_headers(c.github_token)    
        response = requests.get(commits_url, headers=headers)
        if response.status_code == 200:
            commits = response.json()
            line = json.dumps(commits)
                  
            contributor_data = [repo['id'], repo['full_name'], line]
            commits_repos.append(contributor_data)
            contributor_df = pd.DataFrame(commits_repos, columns=columns)   
            s.update_csv_file(c.commits_path, commits_repos)

        else:
            print(f'Failed to retrieve commits. Status code: {response.status_code}')
    json_file.close()  

def get_monthly_commits():
    # TODO group by month
    print(1)


main()