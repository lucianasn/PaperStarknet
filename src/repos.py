import requests

def obter_repositorios_cairo():
    # Substitua 'SEU_TOKEN_GITHUB' pelo seu token de acesso pessoal do GitHub
    token = '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'  # Remova esta linha se não estiver usando um token
    # Configuração do cabeçalho para a requisição
    headers = {'Authorization': f'token {token}'} if token else {}
    # URL da API do GitHub para pesquisa de repositórios com a linguagem Cairo
    url = 'https://api.github.com/search/repositories'
    
    # Parâmetros da consulta para buscar repositórios com a linguagem Cairo
    params = {'q': 'starknet'}
    # Faz a requisição para a API do GitHub
    response = requests.get(url, headers=headers, params=params)
    # Verifica se a requisição foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Converte a resposta JSON para um dicionário
        resultado = response.json()
        # Obtém a lista de itens (repositórios) do resultado
        repositorios = resultado.get('items', [])
        # Lista os nomes dos repositórios
    for repo in repositorios:
            print(repo['full_name'])
    else:
        print(f'Erro na requisição: {response.status_code}')

if __name__ == '__main__':
    obter_repositorios_cairo()