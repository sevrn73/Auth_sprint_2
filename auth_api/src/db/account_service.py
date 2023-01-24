import uuid
from datetime import datetime
from typing import List
from werkzeug.security import generate_password_hash

from src.db.db import db
from src.db.db_models import User, LoginHistory


def get_user_by_login(login: str) -> User:
    user = User.query.filter_by(login=login).first()

    return user


def get_user_by_identity(identity: uuid) -> User:
    user = User.query.filter_by(id=identity).first()

    return user


def add_record_to_login_history(id: uuid, user_agent: str) -> None:
    new_session = LoginHistory(user_id=id, user_agent=user_agent, auth_date=datetime.now())
    db.session.add(new_session)
    db.session.commit()


def create_user(login: str, password: str) -> User:
    hashed_password = generate_password_hash(password)
    new_user = User(login=login, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return new_user


def change_login_in_db(user: User, new_login: str) -> None:
    user.login = new_login
    db.session.commit()


def change_password_in_db(user: User, new_password: str) -> None:
    hashed_password = generate_password_hash(new_password)
    user.password = hashed_password
    db.session.commit()


def get_login_hystory(identity: uuid, page: int, per_page: int) -> List:
    return (
        LoginHistory.query.filter_by(user_id=identity)
        .order_by(LoginHistory.auth_date.desc())
        .paginate(page=page, per_page=per_page)
    )
