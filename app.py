from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import LogIn, SignIn, Delete, Update
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'p0auioç7kmçApqRBhxlÇ23'  # TODO Colocar uma key melhor e em um arquivo .env
jwt = JWTManager(app)
api = Api(app)
api.add_resource(LogIn, '/login')
api.add_resource(SignIn, '/signin')
api.add_resource(Delete, '/user/delete')
api.add_resource(Update, '/user/update')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(port=port, debug=True)
