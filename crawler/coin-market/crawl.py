import psycopg2
import requests
import sys
import logging
import datetime
import time
import os
from bs4 import BeautifulSoup

TIME_SLEEP = os.getenv("TIME_SLEEP")

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

url = os.getenv("WEB_URL")
transfer_url = os.getenv("TRANSFER_URL")

connection = None

def crawl():
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    temp_price = soup.find('span', {'data-test': 'text-cdp-price-display'}).text[1:]
    price = temp_price.replace(",", "")

    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price": price,
        "crawl_at": "\'" + time_now + "\'"
    }

def insert_sql(table_name, data):
    list_field_name = [field for field in data] 
    result_field_name = ','.join(list_field_name)

    data_insert = [value for value in data.values()]
    result_data_insert = ','.join(data_insert)


    return f"""
        INSERT INTO {table_name} ({result_field_name})
        VALUES ({result_data_insert})
    """

try:
    connection = psycopg2.connect(
        user= os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("SERVER_NAME"),
        port="5432",
        database=os.getenv("POSTGRES_DB") 
    )

    cursor = connection.cursor()

    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"Connected to PostgreSQL, version: {db_version}")

    while True:
        data = crawl()
        sql = insert_sql(os.getenv("POSTGRES_TABLE"), data)
        cursor.execute(sql)
        connection.commit()

        time.sleep(int(TIME_SLEEP))

except Exception as error:
    print(f"Error connecting to PostgreSQL: {error}")

finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")