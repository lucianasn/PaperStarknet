import requests

#from ..utils import constants as c

def get_contributors_statistics(full_name, token=None):
    statistics_url = f'https://api.github.com/repos/{full_name}/stats/contributors'

    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    print(statistics_url)
    try:
        response = requests.get(statistics_url, headers=headers)
        response.raise_for_status()

        statistics_devs = response.json()
        __calculate_stats_contributors(statistics_devs)

    except requests.exceptions.RequestException as e:
        print(f'Error retrieving contributor statistics from GitHub: {e}')

######################## Private functions ###############################

def __calculate_stats_contributors(statistics_devs):
    for contributor_stats in statistics_devs:
        contributor = contributor_stats['author']['login']
        total_commits = contributor_stats['total']
        additions = contributor_stats['weeks'][-1]['a']
        deletions = contributor_stats['weeks'][-1]['d']

        print(f'Contributor: {contributor}')
        print(f'Total Commits: {total_commits}')
        print(f'Additions: {additions}')
        print(f'Deletions: {deletions}')
        print('---')
