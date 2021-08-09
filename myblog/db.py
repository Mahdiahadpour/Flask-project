from flask import current_app
from flask import g
from pymongo import MongoClient

#get database for each request
def get_db():
    if "db" not in g:
        client = MongoClient()
        db_name = current_app.config['DATABASE']
        g.db = client[db_name]

    return g.db
