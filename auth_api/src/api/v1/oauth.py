from flask import Blueprint

import uuid
from http.client import BAD_REQUEST, FORBIDDEN, NOT_FOUND

from flask import current_app, request, jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token

from src.oauth.providers import OAuthSignIn
from src.db.oauth_service import create_user_oauth
from src.db.account_service import add_record_to_login_history

from src.db.db_models import User, OAuthAccount


oauth = Blueprint('oauth_helper', __name__)


@oauth.route('/authorize/<provider>')
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@oauth.route('/oauth_callback/<provider>')
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    return jsonify(social_id=social_id, username=username, email=email)
