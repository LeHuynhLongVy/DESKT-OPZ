from pymongo import MongoClient
from bson import json_util


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'Your DB name'
COLLECTION_NAME = 'collectionname'

@app.route("/")
def getDatas():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DB_NAME][COLLECTION_NAME]
    projects = collection.find()
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)