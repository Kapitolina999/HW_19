from flask import request
from flask_restx import Namespace, Resource

from implemented import auth_service

auth_ns = Namespace('auth')

@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        """
        Принимает логин и пароль из Body запроса в виде JSON, проверяет соответствие с данными в БД
        (есть ли такой пользователь, такой ли у него пароль) -> генерирует токены access_token и refresh_token
        и отдает их в виде JSON.
        """
        data = request.json
        username = data['username']
        password = data['password']

        # проверяем, что все поля заполнены
        if None in [username, password]:
            return '', 400

        # генерируем токены access_token и refresh_token
        tokens = auth_service.generation_tokens(username, password)
        return tokens, 201

    def put(self):
        """
        Принимает refresh_token из Body запроса в виде JSON, проверяет refresh_token,
        если токен не истек и валиден — генерирует токены access_token и refresh_token
        и отдает их в виде JSON"""

        data = request.json
        refresh_token = data['refresh_token']
        tokens = auth_service.approve_refresh_token(refresh_token)
        return tokens, 201
