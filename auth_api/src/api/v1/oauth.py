from flask import Blueprint

import uuid
from http.client import BAD_REQUEST, FORBIDDEN, NOT_FOUND

from flask import  current_app as jsonify, request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token

from src.oauth.providers import OAuthSignIn
from src.db.oauth_service import create_user_oauth
from src.db.account_service import add_record_to_login_history

from src.db.db_models import User, OAuthAccount



def oauth_login():
    provider = request.values.get('provider')
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request."}), BAD_REQUEST
    provider_oauth = OAuthSignIn.get_provider(provider)
    if not provider_oauth:
        return jsonify({"msg": "OAuth provider not found."}), NOT_FOUND

    user_info = provider_oauth.callback()
    if not user_info:
        return jsonify({"msg": "Authentication failed."}), FORBIDDEN

    social_id = user_info["social_id"]
    email = user_info["email"]
    service_name = provider_oauth.provider_name
    service_id = provider_oauth.service_id

    account_model = OAuthAccount.query.filter_by(social_id=social_id).first()
    if account_model is None:
        email_exist = User.query.filter_by(email=email).first()
        if email_exist:
            email = None
        user_model = create_user_oauth(email, social_id, service_id, service_name)
    else:
        user_model = User.query.filter_by(id=account_model["user_id"]).first()

    add_record_to_login_history(user_model.id, request.user_agent.string)

    access_token = create_access_token(identity=user_model.id, fresh=True)
    refresh_token = create_refresh_token(identity=user_model.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token)
