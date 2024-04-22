import mysql.connector
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

from alive_progress import alive_bar


data = []

def get_desciption(link):
    response = requests.get(link)
    content = response.content
    site = BeautifulSoup(content, 'html.parser')

    description_body = site.find('div', id='bloco-descricao-sm')

    if(description_body is None):
        return None

    p_description = description_body.find('p')

    return p_description.text

try: 
    connection = mysql.connector.connect(
        host='localhost',
        database='lends_club_api',
        user='sail',
        password='password')
    
    sql_select_Query = "select * from boardgames where description is NULL order by id_bgg desc"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    rows = cursor.fetchall()
    row_count = cursor.rowcount

    update_query = """UPDATE boardgames SET description = %s WHERE id_ludopedia = %s"""
    with alive_bar(row_count) as bar:
        for row in rows:    
            description = str(get_desciption(row[18]))

            if(description is None):
                continue

            id = row[1]
            record = (description, id)
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



