import configparser
from pymongo import MongoClient
from urllib.parse import quote_plus


def connect_to_database():
    config = configparser.ConfigParser()
    config.read('config.ini')
    username = config.get('database', 'username')
    password = config.get('database', 'password')
    cluster_url = config.get('database', 'cluster_url')
    database_name = config.get('database', 'database_name')
    escaped_username = quote_plus(username)
    escaped_password = quote_plus(password)
    url = f"mongodb+srv://{escaped_username}:{escaped_password}@{cluster_url}/{database_name}" \
          f"?retryWrites=true&w=majority"
    client = MongoClient(url)
    db = client.get_database(database_name)
    return db
