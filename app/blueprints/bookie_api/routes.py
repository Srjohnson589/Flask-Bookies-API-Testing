from . import bookie_api

from flask import request, jsonify

from app.models import User, Book, db

# Create a User
@bookie_api.post('/create_user')
def create_user():
    '''
    payload should include
    {
    "name": "",
    "password" : "",
    }
    
    '''
    data = request.get_json()
    new_user = User(name = data['name'], password = data['password'])

    new_user.save()
    return jsonify({
        'status':'ok',
        'message':'User successfully created'
    })