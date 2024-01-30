import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# Crie uma lista para armazenar as linhas do DataFrame
data = []

arquivo = pd.read_csv('boardgames.csv', sep=';', header=0, nrows=10)

contador = 0
for linha in arquivo.itertuples():

    url = linha.link_ludopedia

    response = requests.get(url)
    content = response.content
    site = BeautifulSoup(content, 'html.parser')

    bloco_descricao = site.find('div', class_='mar-btm bg-gray-light pad-all')
    tag_a = bloco_descricao.find('a')

    href = tag_a.get('href')
    
    # Verificar se há uma correspondência antes de tentar acessar grupos
    id_match = re.search(r'/editora/(\d+)/', href)
    editora_id = id_match.group(1) if id_match else None

    editora_name = tag_a.text
    editora_link = tag_a.get('href')

    descrica_body = site.find('div', id='bloco-descricao-sm')
    p_descricao = descrica_body.find('p')

    descricao = p_descricao.text

    # Adicionar dados à lista
    data.append({'id_ludopedia': linha.id_ludopedia,
                 'name': linha.name,
                 'id_editora': editora_id,
                 'editora_name': editora_name,
                 'editora_link': editora_link,
                 'description': descricao})

# Criar DataFrame a partir da lista
df = pd.DataFrame(data)

# Exportar DataFrame para CSV
df.to_csv('editoras.csv', index=False)
