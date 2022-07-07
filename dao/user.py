from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get(self, uid=None):
        if uid:
            return self.session.query(User).get(uid)

        return self.session.query(User).all()

    def get_by_name(self, name):
        return self.session.query(User).filter(User.username == name).one()

    def create(self, data):
        user = User(**data)
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user):
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, uid):
        user = self.get(uid)
        self.session.delete(user)
        self.session.commit()
