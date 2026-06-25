from database.db import db
from models.user import User

def get_all_users():
    return[usr.to_dict() for usr in User.query.all()]

def get_user(uid):
    user = User.query.get(uid)
    return user.to_dict() if user else None

def create_user(uid,name,email):
    user = User(
        uid  = uid,
        name = name,
        email = email
        )
    db.session.add(user)
    db.session.commit()

    return user.to_dict()

def update_user(uid, name, email):
    user = User.query.get(uid)

    if not user:
        return None

    if name:
        user.name = name

    if email:
        user.email = email

    db.session.commit()

    return user.to_dict()


def delete_user(uid):
    user = User.query.get(uid)

    if not user:
        return None

    db.session.delete(user)
    db.session.commit()

    return user.to_dict()