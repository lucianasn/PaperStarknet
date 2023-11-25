import re
import requests
import json
import pandas as pd

from datetime import datetime

from utils import constants as c
from utils import utilities as u
from utils import save_json as s
from repo_info import statsRepo as stats

MAX_ROW_LIST = 1000

def main():
    print("Getting full history ...")
    get_all_fine_grained_commits()
    print("done.")
    # TODO get_stats_repo()

def get_all_fine_grained_commits():
    columns = ['full_name', 'SHA', 'Author', 'Date', 'Message']
    s.create_empty_csv_file(c.commits_csv_path, columns)    
    __backup_all_commits_repos()    
    __get_fine_grained_data(columns)

######################### Private functions #############################

def __get_fine_grained_data(columns):
    commits_list = open(c.commits_json_temp_path, 'r', encoding='utf-8').readlines()
    commit_controller = 0
    
    for commits in commits_list:
        commits = json.loads(commits)
        all_commits = []
        print(f'tamanho {len(commits)}')
        for commit in commits:
            sha = commit['sha']
            author = commit['commit']['author']['name']
            date = commit['commit']['author']['date']
            message = commit['commit']['message']
            full_name = __parse_github_url_commits(commit['url'])
            all_commits.append([full_name, sha, author, date, message])
            commit_controller += 1        
        
        print(f'number of commits in the list before updating the csv file: {commit_controller}')
        if commit_controller >= MAX_ROW_LIST: #To avoid file writting to often
            commit_controller = 0
            contributor_df = pd.DataFrame(all_commits, columns=columns) 
            contributor_df.to_csv(c.commits_csv_path, mode='a', index=False, header=False)  

def __parse_github_url_commits(url):
    ''' The following regular expression pattern is used to extract the full_name for the url to get commits'''
    pattern = r'https://api\.github\.com/repos/([^/]+)/([^/]+)/commits/'

    match = re.search(pattern, url)

    if match:        
        full_name = f"{match.group(1)}/{match.group(2)}"
        return full_name
    else:
        return f'Unable to extract the full name from the URL {url}'

def __backup_all_commits_repos():
    '''This function get all commits from all repos and save in a temp file. This is a raw data.'''
    repos_list = open(c.repositories_path, 'r', encoding='utf-8').readlines()
    headers = u.get_headers(c.github_token)

    for repo in repos_list:
        repo = json.loads(repo)
        full_name = repo['full_name']
        all_commits = []
        page=1
        while True:
            params = {'per_page': 500, 'page': page}
            commits_url = f'{c.GITHUB_API_RV3}{full_name}/commits'
            response = requests.get(commits_url, headers=headers, params=params)

            if response.status_code == 200:
                commits_data = response.json()

                if not commits_data:
                    break

                all_commits.extend(commits_data)
                page += 1
            else:
                return f"Failed to get commits. Status code: {response.status_code}"
        s.update_json_file(c.commits_json_temp_path, all_commits)    

   



main()
