#import requests
#import time
import json

# LINHA DE EXEMPLO
#{'id': 510783426, 
# 'node_id': 'R_kgDOHnHvwg', 
# 'name': 'starknet-cairo-101', 
# 'full_name': 'starknet-edu/starknet-cairo-101', 
#'private': False, 
# 'owner': {'login': 'starknet-edu', 'id': 101595416, 'node_id': 'O_kgDOBg45GA', 'avatar_url': 'https://avatars.githubusercontent.com/u/101595416?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/starknet-edu', 'html_url': 'https://github.com/starknet-edu', 
# 'followers_url': 'https://api.github.com/users/starknet-edu/followers', 
# 'following_url': 'https://api.github.com/users/starknet-edu/following{/other_user}', 
# 'gists_url': 'https://api.github.com/users/starknet-edu/gists{/gist_id}', 
# 'starred_url': 'https://api.github.com/users/starknet-edu/starred{/owner}{/repo}', 
# 'subscriptions_url': 'https://api.github.com/users/starknet-edu/subscriptions', 
# 'organizations_url': 'https://api.github.com/users/starknet-edu/orgs', 
# 'repos_url': 'https://api.github.com/users/starknet-edu/repos', 
# 'events_url': 'https://api.github.com/users/starknet-edu/events{/privacy}', 
# 'received_events_url': 'https://api.github.com/users/starknet-edu/received_events', 
# 'type': 'Organization', 'site_admin': False}, 
# 'html_url': 'https://github.com/starknet-edu/starknet-cairo-101', 
# 'description': 'Learn how to read Cairo code', 'fork': False, 
# 'url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101', 
# 'forks_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/forks', 
# 'keys_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/keys{/key_id}', 
# 'collaborators_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/collaborators{/collaborator}', 
# 'teams_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/teams', 
# 'hooks_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/hooks', 
# 'issue_events_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/issues/events{/number}', 
# 'events_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/events', 
# 'assignees_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/assignees{/user}', 
# 'branches_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/branches{/branch}', 
# 'tags_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/tags', 
# 'blobs_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/git/blobs{/sha}', 
# 'git_tags_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/git/tags{/sha}', 
# 'git_refs_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/git/refs{/sha}', 
# 'trees_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/git/trees{/sha}', 
# 'statuses_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/statuses/{sha}', 
# 'languages_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/languages', 
# 'stargazers_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/stargazers', 

# 'contributors_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/contributors', 
# 'subscribers_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/subscribers', 

# 'subscription_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/subscription', 
# 'commits_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/commits{/sha}', 
# 'git_commits_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/git/commits{/sha}', 
# 'comments_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/comments{/number}', 
# 'issue_comment_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/issues/comments{/number}', 
# 'contents_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/contents/{+path}', 
# 'compare_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/compare/{base}...{head}', 
# 'merges_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/merges', 
# 'archive_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/{archive_format}{/ref}', 
# 'downloads_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/downloads', 
# 'issues_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/issues{/number}', 
# 'pulls_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/pulls{/number}', 
# 'milestones_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/milestones{/number}', 
# 'notifications_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/notifications{?since,all,participating}', 
# 'labels_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/labels{/name}', 
# 'releases_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/releases{/id}', 
# 'deployments_url': 'https://api.github.com/repos/starknet-edu/starknet-cairo-101/deployments', 
# 'created_at': '2022-07-05T15:00:25Z', 
# 'updated_at': '2023-11-17T12:34:10Z', 
# 'pushed_at': '2023-09-12T09:43:20Z', 
# 'git_url': 'git://github.com/starknet-edu/starknet-cairo-101.git', 
# 'ssh_url': 'git@github.com:starknet-edu/starknet-cairo-101.git', 
# 'clone_url': 'https://github.com/starknet-edu/starknet-cairo-101.git', 
# 'svn_url': 'https://github.com/starknet-edu/starknet-cairo-101', 
# 'homepage': '', 
# 'size': 799, 
# 'stargazers_count': 382, 
# 'watchers_count': 382, 
# 'language': 'Cairo', 
# 'has_issues': True, 
# 'has_projects': True, 
# 'has_downloads': True, 
# 'has_wiki': True, 'has_pages': False, 'has_discussions': False, 
# 'forks_count': 232, 'mirror_url': None, 'archived': False, 'disabled': False, 
# 'open_issues_count': 19, 'license': None, 'allow_forking': True, 'is_template': False, 
# 'web_commit_signoff_required': False, 
# 'topics': ['cairo', 'cairo-lang', 'smart-contracts', 'starknet'], 'visibility': 'public', 
# 'forks': 232, 'open_issues': 19, 'watchers': 382, 'default_branch': 'main', 'score': 1.0}

def read_json(fname):
    print("id;full_name;forks_count;visibility;has_wiki;has_downloads;has_projects;size;created_at;updated_at")

    with open(fname, 'r', encoding='utf-8') as file:
        for line in file:
            #print(line)
            data = json.loads(line)
            print(str(data['id']) + ";" + data['full_name'] + ";" + str(data['forks_count']) + ";" + 
                  data['visibility'] + ";" + str(data['has_wiki']) + ";" + str(data['has_downloads']) +
                  ";" + str(data['has_projects']) + ";" + str(data['size']) + ";" + data['created_at'][:10]
                  + ";" + data['updated_at'][:10])

def main():
    read_json( 'repositories.json' )

if __name__ == "__main__":
    main()
