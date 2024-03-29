"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_bcrypt import Bcrypt
from api.models import db, User, ToDos, Contacts, Memos
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api, origins='*')

#Bcrypt to hash passwords stored in DB
bcrypt = Bcrypt()

@api.route('/users', methods=["GET"])
def handle_users():
    users=User.query.all()
    serialized_users = []
    for user in users:
        user = user.serialize()
        serialized_users.append(user)
    return jsonify({
        "message": "These are all of the users",
        "users": serialized_users
    }), 200

@api.route('/todos', methods=['GET'])
@jwt_required()
def handle_get_todos():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user:
        todos = []
        for x in user.todos:
            todos.append(x.serialize())
        return jsonify({
            "message": "These are all of this user's todos",
            "todos": todos
        }), 200
    
@api.route('/todos', methods=['POST'])
@jwt_required()
def handle_add_todos():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user:
        status = request.json.get('status', None)
        task = request.json.get('task', None)
        notes = request.json.get('notes', None)
        new_todo = ToDos(status = status, task = task, notes = notes, user_id = current_user_id)
        db.session.add(new_todo)
        db.session.commit()
        todos = []
        for todo in user.todos:
            todos.append(todo.serialize())
        return jsonify({
            'message': 'ToDo added', 
            'todos': todos
        }), 200
    
@api.route('/todos/<int:todo_id>', methods=['PUT','DELETE'])
@jwt_required()
def handle_modify_todos(todo_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    method = request.method

    if method == 'PUT':
        task_to_update = ToDos.query.filter_by(id = todo_id, user_id = user.id).first()

        if task_to_update:
            new_status = request.json.get('status', None)
            new_notes = request.json.get('notes', None)
            if new_status:
                task_to_update.status = new_status
            if new_notes:
                task_to_update.notes = new_notes
            db.session.commit()
            todos = []
            for todo in user.todos:
                todos.append(todo.serialize())
            return jsonify({
                'message': 'ToDo updated', 
                'todos': todos
            }), 200
    
    if method == 'DELETE':
        task_to_delete = ToDos.query.filter_by(id = todo_id, user_id = user.id).first()

        if task_to_delete:
            db.session.delete(task_to_delete)
            db.session.commit()
            todos = []
            for todo in user.todos:
                todos.append(todo.serialize())
            return jsonify({
                'message': 'ToDo deleted', 
                'todos': todos
            }), 200

@api.route('/contacts', methods=['GET'])
@jwt_required()
def handle_get_contacts():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user:
        contacts = []
        for contact in user.contacts:
            contacts.append(contact.serialize())
        return jsonify({
            'message': 'Here are the user contacts', 
            'contacts': contacts
        }), 200
    
@api.route('/contacts', methods=['POST'])
@jwt_required()
def handle_add_contact():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user:
        name = request.json.get('name', None)
        phone = request.json.get('phone', None)
        email = request.json.get('email', None)
        address = request.json.get('address', None)
        new_contact = Contacts(name = name, phone = phone, email = email, address = address, user_id = current_user_id)
        db.session.add(new_contact)
        db.session.commit()
        contacts = []
        for contact in user.contacts:
            contacts.append(contact.serialize())
        return jsonify({
            'message': 'Contact added', 
            'contacts': contacts
        }), 200

@api.route('/contacts/<int:contact_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def handle_modify_contacts(contact_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    method = request.method

    if method == 'PUT':
        contact_to_update = Contacts.query.filter_by(id = contact_id, user_id = user.id).first()

        if contact_to_update:
            new_name = request.json.get('name', None)
            new_phone = request.json.get('phone', None)
            new_email = request.json.get('email', None)
            new_address = request.json.get('address', None)
            if new_name:
                contact_to_update.name = new_name
            if new_phone:
                contact_to_update.phone = new_phone
            if new_email:
                contact_to_update.email = new_email
            if new_address:
                contact_to_update.address = new_address
            db.session.commit()
            contacts = []
            for contact in user.contacts:
                contacts.append(contact.serialize())
            return jsonify({
                'message': 'Contact updated',
                'contacts': contacts 
            }), 200
        
    if method == 'DELETE':
        contact_to_delete = Contacts.query.filter_by(id = contact_id, user_id = user.id).first()

        if contact_to_delete:
            db.session.delete(contact_to_delete)
            db.session.commit()
            contacts = []
            for contact in user.contacts:
                contacts.append(contact.serialize())
            return jsonify({
                'message': 'Contact deleted',
                'contacts': contacts 
            }), 200

@api.route('/memos', methods=['GET'])
@jwt_required()
def handle_get_memos():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user:
        memos = []
        for memo in user.memos:
            memos.append(memo.serialize())
        return jsonify({
            "message": "These are all of the user's memos",
            "memos": memos
        }), 200

@api.route('/memos', methods=['POST'])
@jwt_required()
def handle_add_memos():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user:
        title = request.json.get('title', None)
        memo_body = request.json.get('memo_body', None)
        new_memo = Memos(title = title, memo_body = memo_body, user_id = current_user_id)
        db.session.add(new_memo)
        db.session.commit()
        memos = []
        for memo in user.memos:
            memos.append(memo.serialize())
        return jsonify({
            "message": "Memo added",
            "memos": memos
        }), 200
    
@api.route('/memos/<int:memo_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def handle_modify_memos(memo_id):
    current_user_id = 1
    user = User.query.get(current_user_id)
    method = request.method

    if method == 'PUT':
        memo_to_update = Memos.query.filter_by(id = memo_id, user_id = user.id).first()

        if memo_to_update:
            new_title = request.json.get('title', None)
            new_memo_body = request.json.get('memo_body', None)
            if new_title:
                memo_to_update.title = new_title
            if new_memo_body:
                memo_to_update.memo_body = new_memo_body
            db.session.commit()
            memos = []
            for memo in user.memos:
                memos.append(memo.serialize())
            return jsonify({
                "message": "Memo updated",
                "memos": memos
            }), 200
        
    if method == 'DELETE':
        memo_to_delete = Memos.query.filter_by(id = memo_id, user_id = user.id).first()

        if memo_to_delete:
            db.session.delete(memo_to_delete)
            db.session.commit()
            memos = []
            for memo in user.memos:
                memos.append(memo.serialize())
            return jsonify({
                "message": "Memo deleted",
                "memos": memos
            }), 200
        
@api.route('/user/new', methods=['POST'])
def handle_add_user():
    first_name = request.json.get('name', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(first_name = first_name, email = email, password = hashed_password)

    if User.query.filter_by(email = email).first() == None:
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(email = email).first()
        return jsonify({
            "message": "user added",
            "user": user.serialize()
        }), 200
    else:
        return jsonify({
            'message': "That email is already in use"
        }), 412
    
@api.route('/user', methods=['POST'])
def handle_signin():
    email = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(email = email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity = user.id)
        return jsonify({
            "message": "User Logged In",
            "token": access_token,
            "name": user.first_name
        }), 200
    elif user is None:
        return jsonify({
            "message": "Bad username or password"
        }), 401
    elif email is None or password is None:
        return jsonify({
            "message" : "Email and Password required"
        }), 400