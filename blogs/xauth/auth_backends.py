from django.contrib.auth.models import AnonymousUser
from xauth import utils as xauth_utils
from rest_framework.authentication import BaseAuthentication



class JWTAuthentication(BaseAuthentication):
    def __init__(self, realm="API"):
        self.realm = realm

    def authenticate(self, request, **kwargs):
        """[Function to extract jwt token for an header]"""
        try:
            auth_header = request.META.get("HTTP_AUTHORIZATION", None)
            if auth_header:
                auth_method, auth_token = auth_header.split(" ", 1)
                if not auth_token:
                    return None
                if not auth_method.lower() == "jwt":
                    return None
                is_user, user = self.verify_access_token(auth_token)
                if not is_user:
                    return AnonymousUser(), None
                return user, None
            else:
                return AnonymousUser(), None

        except:
            pass

    def verify_access_token(self, auth_token):
        """[verify and decode the jwt token  provided]"""
        is_decoded_jwt, user = xauth_utils.decode_jwt(auth_token)
        if not is_decoded_jwt:
            return False, "Oops! Expired credentials. Please log in"
        return True, user[1]
