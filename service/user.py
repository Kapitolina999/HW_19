import base64
import hashlib
import hmac

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get(self, uid=None):
        return self.dao.get(uid)

    def get_by_name(self, name):
        return self.dao.get_by_name(name)

    def create(self, data):
        data['password'] = self._get_hash(data['password'])
        return self.dao.create(data)

    def update(self, data):
        uid = data['id']
        user = self.get(uid)
        user.username = data['username']
        user.password = self._get_hash(data['password'])
        user.role = data['role']
        self.dao.update(user)

    def delete(self, uid):
        self.dao.delete(uid)

    def _get_hash(self, password):
        """
        Хэш-функция
        :param password: пароль пользователя
        :return: хэш-пароль
        """
        return base64.b64encode(hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), PWD_HASH_SALT,
                                                    PWD_HASH_ITERATIONS))

    # def compare_password(self, password, password_hash):
    #     """
    #     сравнение паролей
    #     :param password: проверяемый пароль
    #     :param password_hash: хэш-пароль
    #     :return: bool
    #     """
        # return hmac.compare_digest(base64.b16decode(password_hash),
        #                            hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
        #                                                PWD_HASH_SALT, PWD_HASH_ITERATIONS).decode('utf-8', 'ignore'))

    def compare_passwords(self, password, password_hash):
        return hmac.compare_digest(base64.b64decode(password_hash), base64.b64decode(self._get_hash(password)))

    # hashlib.pbkdf2_hmac(
    #     HASH_NAME,
    #     password.encode('utf-8'),
    #     PWD_HASH_SALT,
    #     PWD_HASH_ITERATOR
    # ).decode('utf-8', 'ignore')

