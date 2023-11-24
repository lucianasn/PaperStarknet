import json
from developers_info import coreDevelopers
from developers_info import statsDevelopers
from utils import constants as c
from utils import save_json as s

def main():
    repo_total_commits = get_all_developers()
    get_contributor_commits(repo_total_commits)

def get_all_developers():
    
    #core_dev_json = open(c.core_dev_json_path, 'w', encoding='utf-8')

    #stats_repo = open(c.stats_repo_path, 'w', encoding='utf-8')

    repos_list = open(c.repositories_path, 'r', encoding='utf-8').readlines()
    repo_total_commits = {}    

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

        print(query_info)
        # get all contributors data and save them in a file
        total_commits_repo = coreDevelopers.get_all_contributors_repo(query_info)

        '''repo_commit = {
            f'{full_name}': total_commits_repo,
            'total_commits': total_commits_repo
        }'''


        repo_total_commits[f'{full_name}'] = total_commits_repo
        #repo_total_commits.append(repo_commit)
    
    return repo_total_commits

    #__extract_core_developers_by_repo(json.loads(devs_json), core_dev_json)


    


def get_contributor_commits(repo_total_commits):
    colaborators_data_json = open(c.colaborators_path, 'r', encoding='utf-8')
    colaborators_data_json = json.load(colaborators_data_json)
    print(repo_total_commits)
    print("Comecando a imprimir para cada repo")
    print(colaborators_data_json)
    print("#############")
    for dev in colaborators_data_json:
        full_name = dev['full_name']
        total_commits = repo_total_commits[f'{full_name}']
        
        print(dev['full_name'])
        print(total_commits)
        coreDevelopers.calculate_core_developers(colaborators_data_json, total_commits)
    
    
    

    
###################### Private Functions #################################


        


def __extract_core_developers_by_repo(repo, core_dev_json):
    full_name = repo['full_name']
    print(full_name)
    #(contributor_commits, total_amount_commits) = coreDevelopers.get_contributor_commits(full_name, c.github_token)
    
    coreDevelopers.calculate_core_developers(contributor_commits, total_amount_commits)
    
    statsDevelopers.get_contributors_statistics(full_name, c.github_token)

    __wrap_save_contributor_info(repo, contributor_commits, core_dev_json)
    
        

def __wrap_save_contributor_info(repo, core_devs, core_dev_json):
    
    for dev in core_devs:
        contributor_data = {
            'id': repo['id'],
            'repo_full_name': repo['full_name'],
            'login': dev['login'],
            'email': dev['email'],
            'commits_count': dev['commits_count']
        }
        core_dev_json.write(json.dumps(contributor_data) + c.NEW_LINE )        
    

main()