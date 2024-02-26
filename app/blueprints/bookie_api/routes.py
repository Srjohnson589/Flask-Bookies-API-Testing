from . import bookie_api

from flask import request, jsonify

from app.models import User, Book, db

# CREATE
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

#CREATE & UPDATE
@bookie_api.post('/add_current_book')
def add_current_book():
    '''
    -if book not in database, first create book
    -remove book from current users other lists
    -add to current list
    
    '''


@bookie_api.post('/add_read_book')
def add_read_book():
    '''
    -if book not in database, first create book
    -remove book from current users other lists
    -add to current list
    
    '''

@bookie_api.post('/add_to_read_book')
def add__to_read_book():
    '''
    -if book not in database, first create book
    -remove book from current users other lists
    -add to current list
    
    '''

# READ - Get all user reading lists

@bookie_api.get('/user_reading_lists')
def user_reading_lists():
    '''
    -takes in a user
    -returns json with current, read, and to read lists
    
    '''

# DELETE - delete a book off a list
    
