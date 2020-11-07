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

#db_drop_and_create_all()

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

    if 'title' not in drink_long or 'recipe' not in drink_long:
        abort(400)
    
    try:
        drink = Drink(title=drink_long['title'],
                      recipe='['+json.dumps(drink_long['recipe'])+']')
        drink.insert()
        return jsonify({
            "success": True,
            "drinks": [drink.long()],
            }), 200

    except:
        abort(422)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def modify_drink(id):
    try:
        drink = Drink.query.get(id)

        if not drink:
            abort(404)
        
        drink_long = {}
        try:
            drink_long = request.get_json()
        except:
            abort(400)
    
        try:
            if 'title' in drink_long:
                drink.title = drink_long['title']
            if 'recipe' in drink_long:
                drink.recipe = '[' + json.dumps(drink_long['recipe']) + ']'
            drink.update()
            
            return jsonify({
                "success": True,
                "drinks": [drink.long()],
                }), 200

        except:
            abort(422)
    except:
        abort(422)


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    try:
        drink = Drink.query.get(id)

        if not drink:
            abort(404)
    
        try:
            drink.delete()
            
            return jsonify({
                "success": True,
                "delete": id,
                }), 200

        except:
            abort(422)
    except:
        abort(422)


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
