import json
import bottle
import time
from bson.objectid import ObjectId
from copy import copy
from bottle import route, run, request, abort
from pymongo import Connection
 
connection = Connection('localhost', 27017)
db = connection.mydatabase
 
@route('/pings', method='POST')
def post_ping():
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = copy(json.loads(data))
    if not entity.has_key('idUser'):
        abort(400, 'No idUser specified')
    if not entity.has_key('idBook'):
        abort(400, 'No idBook specified')
    if not entity.has_key('progress'):
        abort(400, 'No progress specified')
    if not entity.has_key('timestamp'):
        entity['timestamp'] = str(time.time())
    oid = str(ObjectId())
    entity["_id"] = oid
    try:
        db['pings3'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))
     
@route('/pings', method='GET')
def get_ping():
    entities = db['pings3'].find()
    entities = [entity for entity in entities]
    return {"pings": entities}

@route('/users/:id/pings', method='GET')
def get_user_pings(id):
    entities = db['pings3'].find({'idUser':id})
    if not entities:
        abort(404, 'No document with id %s' % id)
    entities = [entity for entity in entities]
    return {"pings": entities}

@route('/books/:id/pings', method='GET')
def get_book_pings(id):
    entities = db['pings3'].find({'idBook':id})
    if not entities:
        abort(404, 'No document with id %s' % id)
    entities = [entity for entity in entities]
    return {"pings": entities}
 
run(host='localhost', port=8080)