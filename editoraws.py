import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

from alive_progress import alive_bar

import mysql.connector 

# Crie uma lista para armazenar as linhas do DataFrame
data = []

try:
    connection = mysql.connector.connect(
        host='localhost',
        database='lends_club_api',
        user='sail',
        password='password')

    sql_select_Query = "select * from ludopedias where editora is null"

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)

    rows = cursor.fetchall()
    row_count = cursor.rowcount   

    update_query = """UPDATE ludopedias SET editora = %s WHERE id_jogo = %s"""

    with alive_bar(row_count) as bar:
        for linha in rows:

            url = linha[5]

            response = requests.get(url)
            content = response.content
            site = BeautifulSoup(content, 'html.parser')
            
            top_main = site.find('div', class_="jogo-top-main")

            if(top_main == None):
                continue

            span = top_main.find_all('span', class_='info-span text-sm')                  
     
            if(len(span[2]) == 0):
                continue

            tag_a = span[2].find('a')

            href = tag_a.get('href') if tag_a else None
            
            # Verificar se há uma correspondência antes de tentar acessar grupos
            # id_match = re.search(r'/editora/(\d+)/', href) if href else None
            # editora_id = id_match.group(1) if id_match else None

            editora_name = tag_a.text if tag_a else None
            editora_link = href

            record = (editora_name, linha[0])
            cursor.execute(update_query, record)

            connection.commit()
            
            bar()

except mysql.connector.Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if connection.is_connected():
        connection.close()
        cursor.close()
        print("MySQL connection is closed")



    
