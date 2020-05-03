from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


class LogIn(Resource):
    def post(self):
        data = request.json
        print(data['email'])
        print(data['password'])

        if data['email'] and data['password']:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            return {'token': access_token}, 200

        else:
            return {'message': 'error'}, 403
