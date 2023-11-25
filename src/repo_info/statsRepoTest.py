import statsRepo as r

#let's test the stats for a single repo
repo_owner = '10k-swap'
repo_name = '10k_swap-contracts'
github_token = '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'

statistics = r.get_repo_statistics(repo_owner, repo_name, github_token)

print("Repository Statistics:")
print(f"Stars: {statistics['stars']}")
print(f"Watchers: {statistics['watchers']}")
print(f"Forks: {statistics['forks']}")
print(f"Created Date: {statistics['created_date']}")
print(f"Pull Requests: {statistics['pull_requests']}")
print(f"Issues: {statistics['issues']}")
print(f"Number of Commits: {statistics['commits']}")