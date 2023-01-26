from flask import Blueprint

from src.api.v1.account import (
    sign_up,
    login,
    logout,
    refresh,
    login_history,
    change_login,
    change_password,
    check_perm,
)
from src.api.v1.roles import create_role, delete_role, change_role, roles_list
from src.api.v1.managing import user_roles, assign_role, detach_role
from src.api.v1.oauth import oauth_login


app_v1_blueprint = Blueprint('v1', __name__)
app_v1_blueprint.add_url_rule('/check_perm', methods=['GET'], view_func=check_perm)

app_v1_blueprint.add_url_rule('/change_login', methods=['POST'], view_func=change_login)
app_v1_blueprint.add_url_rule('/change_password', methods=['POST'], view_func=change_password)
app_v1_blueprint.add_url_rule('/login', methods=['POST'], view_func=login)
app_v1_blueprint.add_url_rule('/login_history', methods=['GET'], view_func=login_history)
app_v1_blueprint.add_url_rule('/logout', methods=['DELETE'], view_func=logout)
app_v1_blueprint.add_url_rule('/refresh', methods=['GET'], view_func=refresh)
app_v1_blueprint.add_url_rule('/sign_up', methods=['POST'], view_func=sign_up)

app_v1_blueprint.add_url_rule('/create_role', methods=['POST'], view_func=create_role)
app_v1_blueprint.add_url_rule('/delete_role', methods=['DELETE'], view_func=delete_role)
app_v1_blueprint.add_url_rule('/change_role', methods=['PUT'], view_func=change_role)
app_v1_blueprint.add_url_rule('/roles_list', methods=['GET'], view_func=roles_list)

app_v1_blueprint.add_url_rule('/user_roles', methods=['GET'], view_func=user_roles)
app_v1_blueprint.add_url_rule('/assign_role', methods=['POST'], view_func=assign_role)
app_v1_blueprint.add_url_rule('/detach_role', methods=['DELETE'], view_func=detach_role)

app_v1_blueprint.add_url_rule('/login_oauth', methods=['POST'], view_func=oauth_login)
