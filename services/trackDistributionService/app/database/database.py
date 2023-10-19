import pymongo
from . import config

cfg: config.Config = config.load_config()

client = pymongo.MongoClient(cfg.mongo_dsn.unicode_string())
db = client.StreamServ
