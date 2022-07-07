import calendar
import datetime

import jwt
from flask import abort

from constants import JWT_SECRET, JWT_ALGO
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generation_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_by_name(username)

        #Аутентификация
        if user is None:
            raise abort(404)

        # Если создание новых токенов, то проходим проверку
        if not is_refresh:
            #Аутентификация пароля
            if not self.user_service.compare_passwords(password, user.password):
                abort(400)

        data = {'username': user.username,
                'role': user.role}

        #Задаем время жизни access_token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        return {'access_token': access_token, 'refresh_token': refresh_token}

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGO])
        username = data['username']
        # т.к. это refresh, то пароль уже не требуем, потому что авторизация уже пройдена
        return self.generation_tokens(username, None, is_refresh=True)
