import requests
import sys
import logging
import datetime
import mysql.connector
import time
import os
import re

TIME_SLEEP = os.getenv("TIME_SLEEP")

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

database = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}
url = os.getenv("WEB_URL")

connection = None

def crawl():
    res = requests.get(url)
    price = re.findall(r'"close":"\d+.\d+"', res.text)[0].split(":")[1].split('"')[1]

    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "price": price,
        "crawl_at": "\"" + time_now + "\""
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
    connection = mysql.connector.connect(**database)
    if connection.is_connected():
        print("Connect to MySQL successfully!")
    
    while (True):
        data = crawl()
        sql = insert_sql(os.getenv("TABLE_NAME"), data)

        print(sql)

        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()

        time.sleep(int(TIME_SLEEP))


except mysql.connector.Error as e:
    print(f"Error when conenct to MySQL: {e}")

finally:
    if connection is not None and connection.is_connected():
        connection.close()
        print("Connect ends!")