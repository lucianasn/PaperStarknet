import requests

def get_contributors(repo_owner, repo_name, token=None):
    contributors_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contributors'
    

    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    

    response = requests.get(contributors_url, headers=headers)
    
    if response.status_code == 200:

        contributors = response.json()
        

        contributor_names = [contributor['login'] for contributor in contributors]
        return contributor_names
    else:
        print(f'Failed to retrieve contributors. Status code: {response.status_code}')
        return []
    
def get_contributors_url(contributors_url, token=None):

    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    response = requests.get(contributors_url, headers=headers)
    
    if response.status_code == 200:
        contributors = response.json()
        
        contributor_names = [contributor['login'] for contributor in contributors]
        return contributor_names
    else:
        print(f'Failed to retrieve contributors. Status code: {response.status_code}')
        return []

# Unit test code
repository_owner = 'starknet-edu'
repository_name = 'starknet-cairo-101'
github_token = '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'  

#@Cristiano this function here below is to use when you have the attributes
contributors = get_contributors(repository_owner, repository_name, github_token)
print(f'Contributors for {repository_owner}/{repository_name}: {contributors}')

#@Cristiano the function get_contributors_url you use to pass the full URL 