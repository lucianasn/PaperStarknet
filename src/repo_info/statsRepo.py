import requests

from utils import constants as c
from utils import save_json as s
from utils import utilities as u

def get_repo_statistics(query):
    base_url = query['url']
    headers = u.get_headers(query['token'])    
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        repo_info = response.json()
        
        stars = repo_info['stargazers_count']
        watchers = repo_info['subscribers_count']
        forks = repo_info['forks_count']
        created_date = repo_info['created_at']
        (languages, cairo) = __get_language(base_url, headers)
        pr_count = __get_number_pr(base_url, headers)
        issues_count = __get_number_issues(base_url, headers)
        commits_count = __get_number_commits(base_url, headers)

        repo_statistics = [query['id'], query['full_name'], languages, cairo, stars, watchers, forks, created_date, pr_count, issues_count, commits_count]

        return repo_statistics

    else:
        return f'Failed to get repository information. Status code: {response.status_code}'


############### Private Functions ####################

def __get_number_pr(base_url, headers):
    pr_url = f'{base_url}/pulls'
    pr_response = requests.get(pr_url, headers=headers)
    return len(pr_response.json())

def __get_number_issues(base_url, headers):
    issues_url = f'{base_url}/issues'
    issues_response = requests.get(issues_url, headers=headers)
    return len(issues_response.json())

def __get_number_commits(base_url, headers):
    commits_url = f'{base_url}/commits'
    commits_response = requests.get(commits_url, headers=headers)
    return len(commits_response.json())

def __get_language(base_url, headers):
    language_url = f'{base_url}/languages'
    language_response = requests.get(language_url, headers)
    cairo = False
    language_info = ''
    if language_response.status_code == 200:
        language_info = language_response.json()
        if 'Cairo' in language_info:
            cairo = True
    return (language_info, cairo)