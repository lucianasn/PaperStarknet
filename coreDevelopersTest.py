import coreDevelopers


repository_owner = 'starknet-edu/starknet-cairo-101'
repository_name = 'starknet-cairo-101'
github_token = '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'  

(contributor_commits, total_amount_commits) = coreDevelopers.get_contributor_commits(repository_owner, github_token)
print(f'Number of commits for each contributor: {contributor_commits}')

sorted_contributors = coreDevelopers.__sort_contributor_info_by_number_commits(contributor_commits)
print('Sorted contributor information:')
for contributor in sorted_contributors:
    print(f'Login: {contributor["login"]}, Email: {contributor["email"]}, Commits: {contributor["commits_count"]}')

core_devs = coreDevelopers.calculate_core_developers(sorted_contributors, total_amount_commits)
print(f'Number of commits for each contributor: {core_devs}')

