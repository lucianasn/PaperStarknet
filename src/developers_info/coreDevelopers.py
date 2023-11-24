import requests
import pandas as pd

from utils import constants as c
from utils import save_json as s
from utils import utilities as u

def get_all_contributors_repo(query_info):
    contributors_url = query_info['contributors_url']
    
    headers = u.get_headers(query_info['token'])    
    response = requests.get(contributors_url, headers=headers)
    
    if response.status_code == 200:
        contributors = response.json()
        
        (contributors_info, total_commits_repo) = __get_contributors_info(query_info, contributors, headers)
        
        return (contributors_info, total_commits_repo)
    else:
        print(f'Failed to retrieve contributors. Status code: {response.status_code}')
        return None

def calculate_core_developers(contributors_info, total_amount_commits):
    floor = total_amount_commits * 0.05
    ceiling = total_amount_commits * 0.8

    accumulated_commits_devs = 0
    
    #for index, row_data in contributors_info.iterrows():
    for row in contributors_info.itertuples(index=True, name='RowData'):
        commits_count = contributors_info.loc[row.Index, 'commits_count'] 
        not_reached_ceiling = accumulated_commits_devs < ceiling
        minimum_dev_contribution = commits_count >= floor

        is_core_dev = not_reached_ceiling and minimum_dev_contribution

        if is_core_dev:
            contributors_info.loc[row.Index, 'core_dev'] = True

        accumulated_commits_devs += commits_count

    

#######################################################################
###                         Private functions                       ###
#######################################################################

def __get_contributors_info(query_info, contributors, headers):
    '''Let's get the commits and emails of each contributor'''
    
    contributor_info = []
    total_commits_repo = 0
    url = query_info['url']


    for contributor in contributors:
        contributor_login = contributor['login']
        contributor_url = f'{url}/commits?author={contributor_login}'
        response = requests.get(contributor_url, headers=headers)

        if response.status_code == 200:
            commits = response.json()
            
            if len(commits) == 0:
                continue

            contributor_email = commits[0]['commit']['author']['email']

            total_commits_repo += len(commits)

            contributor_data = [query_info['id'],query_info['full_name'],contributor_login,contributor_email,len(commits),False]
            contributor_info.append(contributor_data)
        else:
            print(f'Failed to retrieve commits for {contributor_login}. Status code: {response.status_code}')

    return (contributor_info, total_commits_repo)

def sort_contributor_info_by_number_commits_df(contributors, column_to_sort):
    try:
        sorted_dataframe = contributors.sort_values(by=column_to_sort, ascending=False)

        return sorted_dataframe

    except Exception as e:
        print(f"Error sorting DataFrame: {e}")