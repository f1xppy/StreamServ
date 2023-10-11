import pymongo
from app import config

cfg: config.Config = config.load_config()

client = pymongo.MongoClient(cfg.mongo_dsn.unicode_string())
db = client.StreamServ

'''
import pymongo
from app import config

host = config.MONGO_HOST
port = config.MONGO_PORT
username = config.MONGO_USER
password = config.MONGO_PASSWORD
_db = config.MONGO_DB

if username and password:
    mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, _db)
    client = pymongo.MongoClient(mongo_uri)
else:
    client = pymongo.MongoClient(host, port)

db = client[_db]
'''
