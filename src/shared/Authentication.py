#src/shared/Authentication
import jwt
import os
import datetime
from flask import json,Response,request,g
import flask
from functools import wraps
from ..models.UserModel import UserModel


class Auth():
    """
    Auth Class
    """

    @staticmethod
    def generate_token(user_id):
        """
        Generate Token Method
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload,'hhgaghhgsdhdhdd',algorithm='HS256').decode("utf-8")
        except Exception as e:
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': 'error in generating user token'}),
                status=400
            )

    @staticmethod
    def decode_token(token):
        """
        Decode token method
        """
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, 'hhgaghhgsdhdhdd')
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            re['error'] = {'message': 'token expired, please login again'}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {'message': 'Invalid token, please try again with a new token'}
            return re

    # decorator
    @staticmethod
    def auth_required(func):
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            #request.headers["api-token"]= "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODIwNjA4NjQsImlhdCI6MTU4MTk3NDQ2NCwic3ViIjoxfQ.DxdAib_s_GiCuEdUuD7sa322NsMAy2KKfoM38hRQSPM"
           # if 'api-token' not in request.headers:
            #    return Response(
             #      mimetype="application/json",
             #       response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
              #      status=400)
            token = request.headers.get('api-token') or request.headers.get('api-token','eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODIzMjAyMDcsImlhdCI6MTU4MjIzMzgwNywic3ViIjoxfQ.N7H70WjfxhffRWx8TNOFz7nz3UMR_GII2fed0PxkrSg')
            data = Auth.decode_token(token)
            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )

            user_id = data['data']['user_id']
            check_user = UserModel.get_one_user(user_id)
            if not check_user:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'user does not exist, invalid token'}),
                    status=400
                )
            g.user = {'id': user_id}
            return func(*args, **kwargs) #,{'api-token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODIwNjA4NjQsImlhdCI6MTU4MTk3NDQ2NCwic3ViIjoxfQ.DxdAib_s_GiCuEdUuD7sa322NsMAy2KKfoM38hRQSPM'}

        return decorated_auth
