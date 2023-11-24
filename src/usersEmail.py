import requests

def get_user_emails(username, token):
    headers = {
        'Authorization': f'token {token}'
    }    
    
    user_url = f'https://api.github.com/users/{username}'
    response = requests.get(user_url, headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        print(f'user: {user_url}')
        if user_data['email']:
            print(user_data['email'])
            return [user_data['email']]
        else:
            print('User email is not public')
            return []
    else:
        print(f'Failed to retrieve user data. Status code: {response.status_code}')
        return []

# Unit test code
github_username = 'davidmitesh'
github_token = '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'

emails = get_user_emails(github_username, github_token)
print(f'Emails of {github_username}: {emails}')

