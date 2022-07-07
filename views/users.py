from flask_restx import Resource, Namespace
from flask import request

from dao.model.user import UserSchema
from implemented import user_service

user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        users = user_service.get()
        return users_schema.dump(users), 200

    def post(self):
        data = request.json
        user_service.create(data)
        return '', 201


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        user = user_service.get(uid)
        return user_schema.dump(user), 200

    def put(self, uid):
        data = request.json

        if 'id' not in data:
            data['id'] = uid

        user_service.update(data)
        return '', 201

    def delete(self, uid):
        user_service.delete(uid)
        return '', 204
