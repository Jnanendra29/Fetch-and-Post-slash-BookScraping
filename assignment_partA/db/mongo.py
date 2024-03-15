from pymongo import MongoClient

# # connecting to mongodb
mongo_uri = 'mongodb://localhost:27017/'
client = MongoClient(mongo_uri)

# database name
db = client['python_fetching']

# collection names
users_collection = db['users']
posts_collection = db['posts']
