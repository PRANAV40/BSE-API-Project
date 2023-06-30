import os
from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


def connect_to_database():
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    cluster_url = "cluster0.dmwle4q.mongodb.net"
    database_name = "api_data_db"
    escaped_username = quote_plus(username)
    escaped_password = quote_plus(password)
    url = f"mongodb+srv://{escaped_username}:{escaped_password}@{cluster_url}/{database_name}" \
          f"?retryWrites=true&w=majority"
    client = MongoClient(url)
    db = client.get_database(database_name)
    return db
