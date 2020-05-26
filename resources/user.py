from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.user import User
from utils.jwt_validator import validate
import datetime
import hashlib


class LogIn(Resource):
    def post(self):
        data = request.json
        user = User()
        try:
            if user.get_user_by_email(data['email']):
                if user.password == hashlib.md5(str(data['password']).encode('utf-8')).hexdigest():
                    current_user = user.user_id
                    expiration = datetime.timedelta(hours=6)
                    access_token = create_access_token(identity=current_user, expires_delta=expiration)
                    return {
                               'token': access_token,
                               'data': user.user_data(),
                               'success': True
                           }, 200

                else:
                    return {'message': 'Incorrect Password', 'success': False}, 403

            else:
                return {'message': 'Account not found', 'success': False}, 404

        except KeyError as err:
            return {'message': f'{err} is required', 'success': False}, 403


class SignIn(Resource):
    def post(self):
        data = request.json
        user = User()
        try:
            if not user.get_user_by_email(data['email']):
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.birth_date = data['birth_date']
                user.email = data['email']
                user.password = hashlib.md5(str(data['password']).encode('utf-8')).hexdigest()
                if user.create_user():
                    return {'message': 'User created', 'success': True}, 201

                return {'message': 'The user could not be created', 'success': False}, 500

            return {'message': 'The email is already in use', 'success': False}, 400

        except KeyError as err:
            return {'message': f'{err} is required', 'success': False}, 400


class Delete(Resource):
    @jwt_required
    def delete(self):
        token = request.headers['Authorization'].replace('Bearer ', '')
        data = request.json
        user = User()
        if validate(token, data['user_id']):
            if user.get_user_by_id(data['user_id']):
                if user.password == hashlib.md5(str(data['password']).encode('utf-8')).hexdigest():
                    if user.delete_user():
                        return {'message': 'User successfully deleted', 'success': True}, 200

                    return {'message': 'User could not be deleted', 'success': False}, 500

                return {'message': 'Invalid password', 'success': False}, 401

            return {'message': 'The user could not be found', 'success': False}, 400

        return {'message': 'Invalid JWT token', 'success': False}, 400


class Update(Resource):
    @jwt_required
    def put(self):
        token = request.headers['Authorization'].replace('Bearer ', '')
        data = request.json
        user = User()
        if validate(token, data['user_id']):
            if user.get_user_by_id(data['user_id']):
                user_data = user.user_data()
                user_data_keys = list(user_data.keys())
                for data_key in list(data.keys()):
                    if data_key not in user_data_keys:
                        if data_key != 'password':
                            return {'message': f'The attribute "{data_key}" is not accepted', 'success': False}, 400

                if 'password' in list(data.keys):
                    user.password = data['password']
                    if user.update_user():
                        return {'message': 'User password updated', 'success': True}, 200

                    return {'message': 'Failed to update user password', 'success': False}, 500

                for data_key in list(user_data.keys()):
                    user_data[data_key] = data[data_key]

                user.email = user_data['email']
                user.first_name = user_data['first_name']
                user.last_name = user_data['last_name']
                user.birth_date = user_data['birth_date']
                if user.update_user():
                    return {'message': 'User updated', 'success': True}, 200

                return {'message': 'Failed to update user', 'success': False}, 500

            return {'message': 'The user could not be found', 'success': False}, 500

        return {'message': 'Invalid JWT token', 'success': False}, 400
