import coreDevelopers

def get_all_core_developers():
    with open('../dataset/01-repositories-info.json', 'r', encoding='utf-8') as input_file:
        repos_list = input_file.readlines()

    json_file = open('../dataset/core-devs.json', 'w', encoding='utf-8')
    
    for repo in repos_list:
        __extract_core_developers_by_repo(repo, json_file)
    json_file.close()

def main():
    get_all_core_developers()

def __extract_core_developers_by_repo(repo, json_file):
    (contributor_commits, total_amount_commits) = coreDevelopers.get_contributor_commits(repository_owner, github_token)
    print(f'Number of commits for each contributor: {contributor_commits}')

    sorted_contributors = coreDevelopers.__sort_contributor_info_by_number_commits(contributor_commits)
    print('Sorted contributor information:')
    for contributor in sorted_contributors:
        print(f'Login: {contributor["login"]}, Email: {contributor["email"]}, Commits: {contributor["commits_count"]}')

    core_devs = coreDevelopers.calculate_core_developers(sorted_contributors, total_amount_commits)
    print(f'Number of commits for each contributor: {core_devs}')

    for dev in core_devs:

        contributor_data = {
            'id': repo['id'],
            'repo_full_name': repo['full_name'],
            'email': dev['email'],
            'commits_count': dev['commits_count']
        }
        json_file.write(contributor_data + '\n' )