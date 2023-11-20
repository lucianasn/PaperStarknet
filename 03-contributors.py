import requests
import time
import json


def read_json(fname, field):
    dictionary={}
    with open(fname, 'r', encoding='utf-8') as file:
        for line in file:
            #print(line)
            line_json = json.loads(line)
            key = line_json['name']
            request = line_json['owner'][ field ]
            response_json = make_http_request (request)
            add_to_dictionary(dictionary, key, response_json)
    return dictionary

def make_http_request(query):
    time.sleep(10)
    response = requests.get(query)

    if response.status_code == 200:
        print(response.json)
        return response.json()
    else:
        print(f"Erro na solicitação: {response.status_code}")
        return None

def add_to_dictionary(dictionary, key, response_json):
    for item in response_json:
        value = item['id']
        if key not in dictionary:
            dictionary[key]=[]
        if value not in dictionary[key]:
            dictionary[key].append(value)
        print(key, item['id'])
    print(f'repository {key}={len(dictionary[key])}')

def main():
    #read_json( 'teste-01-repositories-info.json', 'followers_url' )
    read_json( '01-repositories-info.json', 'followers_url' )

if __name__ == "__main__":
    main()

