import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from bson.json_util import dumps

cred = credentials.Certificate("../Backend/main/firebase-adminsdk-key.json")
firebase_admin.initialize_app(cred)
fstoredb = firestore.client()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGO_URI'] = 'mongodb://104.198.68.101:27017/tecnicoblautech'

mongo = PyMongo(app)

##ROUTES API-REST ----------------------------------
@app.route('/insertUser', methods=['POST'])
def insertUser():
    req_data = request.get_json();
    print(req_data)
    username = req_data['username']
    name = req_data['name']
    email = req_data['email']
    age = req_data['age']
    password = req_data['password']
    employeeid = req_data['employeeid']
    result = insertDB(username, name, email, age, password, employeeid)
    if (result):
        return "{\"message\":\"Usuario ["+username+"] insertado con éxito.\"}"
    else:
        return "Error al crear usuario.\n"

@app.route('/modifyUser', methods=['PUT'])
def modifyUser():
    req_data = request.get_json();
    username = req_data['username']
    name = req_data['name']
    email = req_data['email']
    age = req_data['age']
    password = req_data['password']
    employeeid = req_data['employeeid']
    result = modifyDB(username, name, email, age, password, employeeid)
    if (result):
        return "{\"message\":\"Usuario ["+username+"] modificado con éxito.\"}"
    else:
        return "Error al modificar usuario.\n"

@app.route('/deleteUser', methods=['DELETE'])
def deleteUser():
    username = request.args.get('username')
    result = deleteDB(username)
    if (result):
        return "{\"message\":\"Usuario ["+username+"] eliminado con éxito.\"}"
    else:
        return "Error al eliminar usuario.\n"

@app.route('/findUsers', methods=['GET'])
def findUsers():
    result = findDB()
    if (result):
        responseObject = {"users": []}
        for x in result:
            responseObject["users"].append(x)

        print(responseObject)
        return dumps(responseObject)
    else:
        return "Error al buscar usuarios.\n"

##API-FUNCTIONS ----------------------------------
def insertDB(username, name, email, age, password, employeeid):
    payload = {'username': username, 'name': name, 'email': email, 'age': age,
               'password': password, 'employeeid': employeeid}
    try:
        doc_ref = fstoredb.collection('usuario').document(username).set(payload)

        return mongo.db.usuario.insert_one(payload)
    except:
        return None


def modifyDB(username, name, email, age, password, employeeid):
    query = {"username": username}
    values = {"$set": {'name': name, 'email': email, 'age': age,
                       'password': password, 'employeeid': employeeid}}
    try:
        values_fstore = {"username": username, 'name': name, 'email': email, 'age': age,
                         'password': password, 'employeeid': employeeid}
        doc_ref = fstoredb.collection('usuario').document(username).set(values_fstore)

        return mongo.db.usuario.update_one(query, values)
    except:
        return None

def deleteDB(username):
    if (username != "admin"):
        query = {"username": username}
        try:
            doc_ref = fstoredb.collection('usuario').document(username).delete()
            return mongo.db.usuario.delete_one(query)
        except:
            return None
    else:
        return None

def findDB():
    try:
        return mongo.db.usuario.find()
    except:
        return None

# START SERVER----------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=4100)
