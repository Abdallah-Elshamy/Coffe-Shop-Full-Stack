import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

## ROUTES

@app.route('/drinks')
def get_drinks():
    try:
        drinks = [drink.short() for drink in Drink.query.all()]
        return jsonify({
            "success": True,
            "drinks": drinks,
            }), 200
    except:
        abort(422)


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    try:
        drinks = [drink.long() for drink in Drink.query.all()]
        return jsonify({
            "success": True,
            "drinks": drinks,
            }), 200
    except:
        abort(422)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink():
    drink_long = {}
    try:
        drink_long = request.get_json()
    except:
        abort(400)

    if not drink_long['title'] or not drink_long['recipe']:
        abort(400)
    
    try:
        drink = Drink(title=drink_long['title'],
                      recipe=drink_long['recipe'])
        drink.insert()
        return jsonify({
            "success": True,
            "drinks": [drink.short()],
            }), 200

    except:
        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "Bad Request"
                    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                    "success": False, 
                    "error": error.status_code,
                    "message": error.error
                    }), error.status_code
