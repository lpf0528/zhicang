from django.core.exceptions import PermissionDenied

from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.deprecation import MiddlewareMixin  # 修改为MiddlewareMixin
from threading import local

_user = local()


class CurrentUserMiddleware(MiddlewareMixin):  # 继承MiddlewareMixin
    def __init__(self, get_response):
        self.get_response = get_response
        self.authenticator = JWTAuthentication()  # 实例化JWTAuthentication

    def __call__(self, request):
        # 获取并解析令牌
        header = self.authenticator.get_header(request)
        user = request.user
        if header is not None:
            raw_token = self.authenticator.get_raw_token(header)
            if raw_token is not None:
                try:
                    validated_token = self.authenticator.get_validated_token(raw_token)
                    user = self.authenticator.get_user(validated_token)
                    if not user:
                        raise PermissionDenied("Invalid token")
                except Exception as e:
                    raise PermissionDenied("Invalid token") from e
        _user.value = user
        response = self.get_response(request)
        return response

    @staticmethod
    def get_current_user():
        return getattr(_user, 'value', None)
