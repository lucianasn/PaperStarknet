
def get_headers(token):
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'

    return headers