from datetime import timedelta
from flask import Flask
from flask import send_from_directory
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from src.db.db import init_db
from src.api.v1.api_v1_blueprint import app_v1_blueprint
from src.core.config import project_settings, redis_settings
from src.cache.redis_cache import redis_cache
from src.db.roles_service import get_user_primary_role
from src.api.v1.admin import create_admin_role

SWAGGER_URL = '/docs/'
API_URL = '/static/swagger_config.yaml'
swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = project_settings.SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=redis_settings.ACCESS_EXPIRES_IN_SECONDS)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=redis_settings.REFRESH_EXPIRES_IN_SECONDS)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        """
        Callback function to check if a JWT exists in the redis blocklist
        """
        jti = jwt_payload['jti']
        token_in_redis = redis_cache._get(jti)
        return token_in_redis is not None

    @jwt.additional_claims_loader
    def add_roles_to_access_token(identity):
        return get_user_primary_role(identity)

    app.register_blueprint(swagger_blueprint)
    app.register_blueprint(app_v1_blueprint, url_prefix='/v1')
    app.cli.add_command(create_admin_role)

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    return app


def start_app():
    app = create_app()
    init_db(app)
    app.app_context().push()
    return app


if __name__ == '__main__':
    start_app()
