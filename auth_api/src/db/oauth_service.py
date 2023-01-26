import random
import string
from werkzeug.security import generate_password_hash

from src.db.db import db
from src.db.db_models import User, OAuthAccount
from src.db.account_service import create_user


def generate_password(size=20):
    chars = string.ascii_letters + string.punctuation + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def get_account():
    account = OAuthAccount()
    db.session.add(account)
    db.session.commit()


def add_record_to_oauth_account(user_id, social_id, service_id, service_name):
    account = OAuthAccount(user_id=user_id, social_id=social_id, service_id=service_id, service_name=service_name)
    db.session.add(account)
    db.session.commit()


def create_user_oauth(username, email, social_id, service_id, service_name) -> User:
    login = username
    password = generate_password()
    new_user = create_user(login, password, email)
    add_record_to_oauth_account(new_user.id, social_id, service_id, service_name)
    return new_user
