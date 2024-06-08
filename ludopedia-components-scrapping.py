import mysql.connector
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from collections.abc import Mapping

from alive_progress import alive_bar



data = []

def get_components(link):
    response = requests.get(link)
    content = response.content
    site = BeautifulSoup(content, 'html.parser')

    component_body = site.find('div', id='bloco-componentes-sm')

    if(component_body is None):
        return None

    p_component = component_body.find('p')

    return p_component.text

try: 
    connection = mysql.connector.connect(
        host='localhost',
        database='laravel',
        user='root')
    
    sql_select_Query = "select * from boardgames where components is NULL order by id_bgg desc"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    rows = cursor.fetchall()
    row_count = cursor.rowcount

    update_query = """UPDATE boardgames SET components = %s WHERE id_ludopedia = %s"""
    with alive_bar(row_count) as bar:
        for row in rows:    
            components = str(get_components(row[18]))

            if(components is None):
                continue

            id = row[1]
            record = (components, id)
            cursor.execute(update_query, record)
            connection.commit()
            bar()      

    print("Total number of rows in boardgames is: ", cursor.rowcount)

except mysql.connector.Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if connection.is_connected():
        connection.close()
        cursor.close()
        print("MySQL connection is closed")



