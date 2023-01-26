import datetime
import uuid
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from src.db.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<User {self.login}>"


class LoginHistory(db.Model):
    __tablename__ = 'login_history'
    __table_args__ = (
        UniqueConstraint('id', 'auth_date'),
        {
            'postgresql_partition_by': 'RANGE (auth_date)',
        },
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id))
    user_agent = db.Column(db.String, nullable=False)
    auth_date = db.Column(db.DateTime, nullable=False, primary_key=True)


class OAuthAccount(db.Model):
    __tablename__ = "oauth_accaunt"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    social_id = db.Column(db.String, nullable=False)
    service_id = db.Column(db.Text, nullable=False)
    service_name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<OAuthAccount {self.service_name}:{self.user_id}>"


class Roles(db.Model):
    __tablename__ = "roles"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Roles {self.name}>"


class UsersRoles(db.Model):
    __tablename__ = "users_roles"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id))
    role_id = db.Column(UUID(as_uuid=True), ForeignKey(Roles.id))
