from typing import Optional, Dict

from flask import current_app, url_for, request
from rauth import OAuth2Service


class OAuthSignIn:
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config["OAUTH_CREDENTIALS"][provider_name]
        self.consumer_id = credentials["id"]
        self.consumer_secret = credentials["secret"]
        self.consumer_redirect_uri = credentials["redirect_uri"]

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for("oauth_callback", provider=self.provider_name, _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super(YandexSignIn, self).__init__("yandex")
        self.service = OAuth2Service(
            name="yandex",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://oauth.yandex.ru/authorize",
            access_token_url="https://oauth.yandex.ru/token",
            base_url="https://oauth.yandex.ru/",
        )
        self.service_id = "01"

    def callback(self) -> Optional[Dict]:
        access_token = request.json.get("access_token")
        if not access_token:
            return None
        oauth_session = self.service.get_session(token=access_token)
        user_data = oauth_session.get("info?format=json").json()
        return {
            "social_id": f'yandex::{user_data["client_id"]}',
            "email": user_data["default_email"],
        }


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__("google")
        self.service = OAuth2Service(
            name="google",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            # authorize_url="",
            # base_url="",
        )
        self.service_id = "02"

    def get_user_info(self) -> Optional[Dict]:
        access_token = request.json.get("access_token")
        if not access_token:
            return None
        oauth_session = self.service.get_session(token=access_token)
        user_data = oauth_session.get("userinfo").json()
        return {
            "social_id": f'google::{user_data["id"]}',
            "email": user_data["email"],
        }
