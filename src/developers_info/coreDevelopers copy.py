import requests

from utils import constants as c
from utils import save_json as s
from utils import utilities as u

def get_all_contributors_repo(query_info):
    #url = query_info['url']
    contributors_url = query_info['contributors_url']#f'{url}/contributors'
    
    headers = u.get_headers(query_info['token'])    
    response = requests.get(contributors_url, headers=headers)
    
    if response.status_code == 200:
        contributors = response.json()
        print("pegando os contributors")
        (contributors_info, total_commits_repo) = __get_contributors_info(query_info, contributors, headers)
        s.update_json_file(c.colaborators_path, contributors_info)
        
        return total_commits_repo
    else:
        print(f'Failed to retrieve contributors. Status code: {response.status_code}')
        return None

'''
def get_contributor_commits(full_name, token=None):
    url = f'{c.GITHUB_API_RV3}{full_name}'#f'{GITHUB_API_RV3}{repo_owner}/{repo_name.}'
    contributors_url = f'{url}/contributors'
    
    print(url)
    print(contributors_url)

    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    response = requests.get(contributors_url, headers=headers)
    
    if response.status_code == 200:
        contributors = response.json()
        
        contributors_info = __get_contributors_info(contributors, headers, url)
        
        return contributors_info
    else:
        print(f'Failed to retrieve contributors. Status code: {response.status_code}')
        return None
'''

def calculate_core_developers(contributors_info, total_amount_commits):
    floor = total_amount_commits * 0.05
    ceiling = total_amount_commits * 0.8

    contributors_info = __sort_contributor_info_by_number_commits(contributors_info)

    accumulated_commits_devs = 0
    #core_devs = []
    
    print("### repo do contributor")
    for contributor in contributors_info:
        print(contributor['full_name'])
        not_reached_ceiling = accumulated_commits_devs < ceiling
        minimum_dev_contribution = contributor['commits_count'] >= floor

        is_core_dev = not_reached_ceiling and minimum_dev_contribution

        if is_core_dev:
            contributor['core_dev'] = True

        #core_devs.append(contributor)
        accumulated_commits_devs += contributor['commits_count']

    #return core_devs

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
        print(contributor_url)
        response = requests.get(contributor_url, headers=headers)

        if response.status_code == 200:
            commits = response.json()
            
            if len(commits) == 0:
                continue

            contributor_email = commits[0]['commit']['author']['email']

            total_commits_repo += len(commits)

            contributor_data = {
                'id': query_info['id'],
                'full_name': query_info['full_name'],
                'login': contributor_login,
                'email': contributor_email,
                'commits_count': len(commits),
                'core_dev': False
            }

            contributor_info.append(contributor_data)
            print(contributor_info)
        else:
            print(f'Failed to retrieve commits for {contributor_login}. Status code: {response.status_code}')

    __sort_contributor_info_by_number_commits(contributor_info)
    return (contributor_info, total_commits_repo)


def __sort_contributor_info_by_number_commits(contributors_info):
    sorted_contributors = sorted(contributors_info, key=lambda x: x['commits_count'], reverse=True)
    return sorted_contributors
