
import run
from flask_restful import Resource
from flask_jwt_extended import *

class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
