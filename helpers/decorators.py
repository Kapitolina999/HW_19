import jwt
from flask import request, abort

from constants import JWT_SECRET, JWT_ALGO


def auth_required(func):
    def wrapper(*args, **kwargs):

        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        # token = data.split('Bearer ')[-1]
        try:
            jwt.decode(data, JWT_SECRET, algorithms=[JWT_ALGO])
        except Exception as e:
            print('JWT decode Exception', e)
            abort(401)

        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    """
    проверяет права пользователя
    """
    def wrapper(*args, **kwargs):

        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        except Exception as e:
            print('JWT decode Exception', e)
            abort(401)

        role = user['role']
        if role != 'admin':
            abort(403)
        return func(*args, **kwargs)
    return wrapper







