import requests
import time
import json

def get_repository_info(query):
    url = f'https://api.github.com/search/repositories?q={query}&page=1'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        total_count = data['total_count']
        total_pages = int(response.headers['Link'].split(',')[-1].split(';')[0].split('page=')[-1].strip('>"'))
        return total_count, total_pages
    else:
        print(f"Erro na solicitação: {response.status_code}")
        return 0, 0

def get_repositories(query, page):
    url = f'https://api.github.com/search/repositories?q={query}&page={page}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()['items']
    else:
        print(f"Erro na solicitação: {response.status_code}")
        return None

def main():
    query = "starknet cairo"  # String de pesquisa

    total_count, total_pages = get_repository_info(query)
    if total_count == 0 or total_pages == 0:
        print("Não foi possível obter a informação sobre repositórios.")
        return

    print(f"Total de repositórios disponíveis: {total_count}")
    print(f"Total de páginas disponíveis: {total_pages}")

    json_file = open('01-repositories-info.json', 'w', encoding='utf-8')

    counter = 0
    for page in range(0, total_pages+1):
        repositories = get_repositories(query, page)

        if repositories:
            print(f"\nRepositórios na página {page} com as strings 'starknet' e 'cairo':\n")
            for repo in repositories:
                line = json.dumps(repo)
                json_file.write( line + '\n' )
                time.sleep(1)
                counter+=1
                print('counter=',counter, ' page=', page)
        else:
            print("Nenhum repositório encontrado.")
    json_file.close()


if __name__ == "__main__":
    main()
