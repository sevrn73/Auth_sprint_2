import random
import string
import uuid
from werkzeug.security import generate_password_hash

from src.db.db import db
from src.db.db_models import User, OAuthAccount


def generate_password(size=20):
    chars = string.ascii_letters + string.punctuation + string.digits
    return "".join(random.choice(chars) for _ in range(size))


def get_account():
    account = OAuthAccount()
    db.session.add(account)
    db.session.commit()


def add_record_to_oauth_account(user_id, social_id, service_id, service_name):
    account = OAuthAccount(user_id=user_id, social_id=social_id, service_id=service_id, service_name=service_name)
    db.session.add(account)
    db.session.commit()


def create_user_oauth(email, social_id, service_id, service_name) -> User:
    login = uuid.uuid4()
    password = generate_password()
    hashed_password = generate_password_hash(password)
    new_user = User(login=login, password=hashed_password, email=email)
    add_record_to_oauth_account(new_user.id, social_id, service_id, service_name)
    return new_user
