###################################################################
# imports
###################################################################
import requests
import time
import json

from utils import constants as c

###################################################################
# main function
###################################################################
def main():
    # open index of repositories: each line stores one repository
    with open('../dataset/index-of-repositories.txt', 'r', encoding='utf-8') as input_file:
    #with open('index-of-repositories-teste.txt', 'r', encoding='utf-8') as input_file:
        repos_list = input_file.readlines()

    # create output json file
    json_file = open('01-repositories-info.json', 'w', encoding='utf-8')

    # process each line
    counter = 0
    for repo in repos_list:
        get_repository_summary(repo, json_file)
        counter += 1
        print(f'Repo: {counter}/{len(repos_list)}')

    # close output json file
    json_file.close()

    # print the output file created
    print('Created file: "01-get-repositories-info.json"')


###################################################################
# function receives the list of repositories or users
# and issues http requests to get the repository data summary
###################################################################
def get_repository_summary(param, json_file):
    # remove whitespaces and convert to lowercase
    param = str(param).strip().lower()

    # find out if this is an "user" or "repo"
    url = param.split('/')

    if len(url)==4:
        # this is a user: we must get the list of repos
        user = url[3]
        api_url = f'https://api.github.com/users/{user}/repos'
        response = make_http_request(api_url)

        for repo in response:
            if repo and str(repo['language']).lower() == "cairo":
                line = json.dumps(repo)
                json_file.write( line + '\n' )

    elif len(url)==5:
        # this is a repo
        user = url[3]
        repo = url[4]
        api_url = f'https://api.github.com/repos/{user}/{repo}'
        repo = make_http_request(api_url)
        if repo:
            repo = json.dumps(repo)
            json_file.write( repo + '\n' )
    else:
        # garbage
        print (f'Unexpected input: {param}')
    return


###################################################################
# helper function to make http requests using the REST API
###################################################################
def make_http_request( api_url ):

    headers = {}
    headers['Authorization'] = f'token {c.github_token}'

    # always sleep before making a request
    time.sleep(2)
    # make http request
    response = requests.get(api_url, headers=headers)
    print(api_url)
    #print(response.status_code)
    #print(response.headers)

    # check for success
    if response.status_code == 200:
        return response.json()

    # error while making http request
    print(f"Error while making http request status {response.status_code}")
    return None #or better exit(1)?


###################################################################
# helper to call the main function
###################################################################
if __name__ == "__main__":
    main()