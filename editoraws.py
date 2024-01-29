import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

url = "https://ludopedia.com.br/jogo/dungeons-dragons-5th-edition-player-s-handbook"

response = requests.get(url)

content = response.content
site = BeautifulSoup(content, 'html.parser')

bloco_descricao = site.find('div', class_='mar-btm bg-gray-light pad-all')
tag_a = bloco_descricao.find('a')

href = tag_a.get('href')
id_match = re.search(r'/editora/(\d+)/', href)

editora_id = id_match.group(1)
editora_name = tag_a.text
editora_link = tag_a.get('href')

descrica_body = site.find('div', id='bloco-descricao-sm')
p_descricao = descrica_body.find('p')

descricao = p_descricao.text

# dataframe

df = pd.DataFrame({'id': [editora_id], 'name': [editora_name], 'link': [editora_link], 'descricao': [descricao]})


# exportação
df.to_csv('editoras.csv', index=False)

