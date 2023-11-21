import requests

GITHUB_API_RV3 = "https://api.github.com/repos/"


def get_contributor_commits(full_name, token=None):
    url = f'{GITHUB_API_RV3}{full_name}'#f'{GITHUB_API_RV3}{repo_owner}/{repo_name.}'
    contributors_url = f'{url}/contributors'

    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'

    response = requests.get(contributors_url, headers=headers)

    if response.status_code == 200:
        contributors = response.json()

        (contributors_info, total_commits_repo) = __get_contributors_info(contributors, headers, url)

        return (contributors_info, total_commits_repo)
    else:
        print(f'Failed to retrieve contributors. Status code: {response.status_code}')
        return None

def calculate_core_developers(contributors_info, total_amount_commits):
    floor = total_amount_commits * 0.05
    ceiling = total_amount_commits * 0.8
    print('TOTAL COMMITS')
    print(total_amount_commits)
    contributors_info = __sort_contributor_info_by_number_commits(contributors_info)

    accumulated_commits_devs = 0
    core_devs = []
    
    for contributor in contributors_info:

        not_reached_ceiling = accumulated_commits_devs < ceiling
        minimum_dev_contribution = contributor['commits_count'] >= floor

        is_core_dev = not_reached_ceiling and minimum_dev_contribution

        if is_core_dev:
            core_devs.append(contributor)

        accumulated_commits_devs += contributor['commits_count']

    return core_devs

#######################################################################
###                         Private functions                       ###
#######################################################################

def __get_contributors_info(contributors, headers, url):
    '''Let's get the commits and emails of each contributor'''
    contributor_info = []
    total_commits_repo = 0

    for contributor in contributors:
        contributor_login = contributor['login']
        contributor_url = f'{url}/commits?author={contributor_login}'
        
        response = requests.get(contributor_url, headers=headers)

        if response.status_code == 200:
            commits = response.json()
            contributor_email = commits[0]['commit']['author']['email']

            total_commits_repo += len(commits)

            contributor_data = {
                'login': contributor_login,
                'email': contributor_email,
                'commits_count': len(commits)
            }

            contributor_info.append(contributor_data)
        else:
            print(f'Failed to retrieve commits for {contributor_login}. Status code: {response.status_code}')
    return (contributor_info, total_commits_repo)

def __sort_contributor_info_by_number_commits(contributors_info):
    sorted_contributors = sorted(contributors_info, key=lambda x: x['commits_count'], reverse=True)
    return sorted_contributors
