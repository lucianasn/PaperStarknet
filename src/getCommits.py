import requests
import pandas as pd
import json    
import datetime
import os
import csv
import time 

GITHUB_API_V4 = 'https://api.github.com/graphql'
GITHUB_URL = "https://github.com/"
GITHUB_API_UV3 = "https://api.github.com/users/"
GITHUB_API_RV3 = "https://api.github.com/repos/"

FILE_COMMITS = 'commits.csv'

tokens = ['be10486cc9ca26b11447105dccb593c2f455fd15', #luciana
'7a779a7343187bddd4679d8ca8edb6de2c5597a5', #cristiano
'acaef496fb6ad01c77f5e868d8c3a671d0990e8f', #luciana
]


def get_users(nameWithOwner, user, access_token='2315b455166c7945da88214420281158025c834d'):
    dataFrame1 = None
    url = nameWithOwner.split("/")
    name = "users/"+url[1]+"_users.csv"
    
    if (os.path.exists(name)):
        dataFrame1 = pd.read_csv(name)

        for i,u in dataFrame1.iterrows():
            if (u['login'] == user):
                return u['id']
    else:
        with open(name, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(['id','node_id','login','name','company','location','email','created_at'
])
  
    headers = {'Authorization': 'token ' + access_token}

    response = requests.get(GITHUB_API_UV3+user, headers=headers);
    json_response = json.loads(response.text)

    item = json_response
    if ('id' not in item):
        df = pd.read_csv('user_id.csv')
        user_id = df['id']
        item['id'] = user_id
        item['node_id'] = "\\N"
        item['login'] = user
        item['name'] = user
        item['company'] = "\\N"
        item['location'] = "\\N"
        item['email'] = "\\N"
        item['created_at'] = "\\N"
        df['id'] += 1
        df.to_csv("user_id.csv", index=False)
    else:
        item['created_at'] = (item['created_at']).replace("T", " ")[:19]
    
        for k, v in item.items():
            if (not v):
                item[k] = "\\N"
        
    users = []
    users.append(item)

    dataFrame2 = pd.DataFrame(users, columns=["id", "node_id", "login", "name", "company", "location", "email", "created_at"])
    dataFrame2['id'] = dataFrame2['id'].astype('int')
    
    if (dataFrame1 is not None): 
        dataFrame1 = dataFrame1.append(dataFrame2)
    else:
        dataFrame1 = dataFrame2
        
    dataFrame1.to_csv(name, index=False)

    return(int(item['id']))


def get_commits(nameWithOwner, project_id, access_token='2315b455166c7945da88214420281158025c834d'):
    '''
        Function used to retrieve commits for a particular project
    '''
    df_Dataset = None
    id = 1
    page = 1
    commits = []

    if (os.path.getsize(FILE_COMMITS) > 0):
        (id, df_Dataset) = __get_id(project_id)        
    
    json_response = __make_request(nameWithOwner, page, access_token)
    
    while json_response:
        print("Page: "+str(page))
        commits += json_response
        page += 1
        json_response = __make_request(nameWithOwner, page, access_token)

    print(len(commits))

    commits = __process_commits(commits, nameWithOwner, project_id, id)            

    __save_commits_csv(commits, df_Dataset)


#####################################################
####            private functions               #####
#####################################################

def __get_id(project_id):
    dataFrame1 = pd.read_csv(FILE_COMMITS)

    for i,c in dataFrame1.iterrows():
        if (c['project_id'] == project_id):
            return
        
    id = dataFrame1["id"].iloc[-1]+1
    return (id, dataFrame1)


def __make_request(nameWithOwner, page, access_token):
    headers = {'Authorization': 'token ' + access_token}
    response = requests.get(GITHUB_API_RV3+nameWithOwner+'/commits?page='+str(page)+'&per_page=100', headers=headers);
    return json.loads(response.text) 


def __process_commits(commits, nameWithOwner, project_id, id):
    for i,c in enumerate(commits):
        c.update({'id':id+i})
        
        if (c['author'] is None or 'login' not in c['author'].keys()):
            author_id = get_users(nameWithOwner, c['commit']['author']['name'])
            if (c['committer'] is None or c['commit']['author']['name'] == c['commit']['committer']['name'] or 'login' not in c['committer']):
                committer_id = author_id
            else:
                committer_id = get_users(nameWithOwner, c['committer']['login'])
        else: 
            author_id = get_users(nameWithOwner, c['author']['login'])
            if (c['committer'] is None or 'login' not in c['committer'] or c['author']['login'] == c['committer']['login']):
                committer_id = author_id
            else:
                committer_id = get_users(nameWithOwner, c['committer']['login'])
        
        c.update({'author_id': author_id})
        c.update({'committer_id': committer_id})
        c.update({'project_id': project_id}) 
        c.update({'created_at': (c['commit']['author']['date']).replace("T", " ")[:19]}) 

    for k,v in c.items():
        if (not v):
            c[k] = "\\N"


def __save_commits_csv(commits, df_Dataset):
    df_temp_commits = pd.DataFrame(commits, columns=["id", "node_id", "sha", "author_id", "committer_id", "project_id", "created_at"])
    df_temp_commits['id'] = df_temp_commits['id'].astype('int')
        
    if (df_Dataset is not None): 
        df_Dataset = df_Dataset.append(df_temp_commits)
    else:
        df_Dataset = df_temp_commits
        
    df_Dataset.to_csv(FILE_COMMITS, index=False)