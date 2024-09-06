import datetime
import os
from pickle import NONE
from django.utils import timezone
import jwt
import random
import string
from xauth import models as xauth_models
from xuser import models as user_models
from xauth import exceptions as xauth_exceptions
from xauth import models as xauth_models


def find_user(username=None, entity=None):# -> user_models.CustomUser:
    """
    [Find user by username]
    """
    if username == None:
        raise xauth_exceptions.UserNotFound
    
    if entity.lower() != 'admin':
        try:
            user = user_models.CustomUser.objects.get(user_name=username)
            return user
        except:
            raise xauth_exceptions.UserNotFound  
    else:
        try:
            user = user_models.AdminUser.objects.get(user_name=username)
            return user
        except:
            raise xauth_exceptions.UserNotFound
        
def create_jwt_token(user, platform, entity):
    token_filter = {"user":f"{user.id}", "platform":f"{platform}"}
    
    if entity.lower() != 'admin':
        user_tokens = xauth_models.AuthToken.objects.filter(**token_filter)
    else:
        user_tokens = xauth_models.AdminAuthToken.objects.filter(**token_filter)

    # user_tokens = xauth_models.AuthToken.objects.filter(**token_filter)
    
    if user_tokens.count() <= 0:
        jwt_token = encode_jwt(user, platform=platform, entity=entity)
    else:
        curr_token = user_tokens[0]
        if curr_token.expiry_date >= timezone.now():
            curr_token.expiry_date =  timezone.now() + datetime.timedelta(hours=72)
            curr_token.save()
            jwt_token = regenerate_jwt(user=user, hours=72, platform=platform, token=curr_token.token, entity=entity)

        if curr_token.expiry_date < timezone.now():
            curr_token.delete()
            jwt_token = encode_jwt(user, platform=platform, entity=entity)
    
    return jwt_token




def encode_jwt(user, platform="API", entity=None):
    """
    Generates Auth Token
    :return: string
    """

    if entity.lower() != 'admin':
        token = xauth_models.AuthToken.objects.create(
            token="".join(random.choice(string.ascii_letters) for i in range(7)),
            user_id=user.id,
            platform=platform,
            expiry_date = timezone.now() + datetime.timedelta(hours=72)
        )
        payload = {
            "exp": timezone.now() + datetime.timedelta(hours=72),
            "iat": timezone.now(),
            "sub": user.user_name,
            "token": token.token,
            "platform": platform,
            "entity": entity
        }
    else:
        token = xauth_models.AdminAuthToken.objects.create(
            token="".join(random.choice(string.ascii_letters) for i in range(7)),
            user_id=user.id,
            platform=platform,
            expiry_date = timezone.now() + datetime.timedelta(hours=72)
        )
        payload = {
            "exp": timezone.now() + datetime.timedelta(hours=72),
            "iat": timezone.now(),
            "sub": user.user_name,
            "token": token.token,
            "platform": platform,
            "entity": entity
        }
    return jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm="HS256")

def regenerate_jwt(user, hours,  platform, token, entity):
    """
    Re-generates Auth Token
    :return: string
    """
    payload = {
        "exp": timezone.now() + datetime.timedelta(hours=hours),
        "iat": timezone.now(),
        "sub": str(user.user_name),
        "token":token,
        "platform": platform,
        "entity": entity
    }
    return jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm="HS256")

def decode_jwt(jwt_token) -> dict:
    """
    Validates the auth token and return encoded payload
    :param auth_token:
    :return: bool|dict
    """
    try:
        payload = jwt.decode(
            jwt_token, os.environ.get('SECRET_KEY'), algorithms="HS256")
        entity = payload.get('entity')
        if entity.lower() != 'admin':
            auth_token = xauth_models.AuthToken.objects.filter(
                token=payload["token"])
        else:
            auth_token = xauth_models.AdminAuthToken.objects.filter(
                token=payload["token"])
        if not auth_token.exists():
            raise xauth_exceptions.InvalidJwtToken
        else:
            return True, (payload, auth_token.first().user)
    except Exception as e:
        print(e)
        return False, xauth_exceptions.InvalidJwtToken


def destroy_jwt(jwt_token: str, all=False, entity=None):
    """
    Validate jwt token and delete token from the database
    :param jwt_token: str
    :param all: bool
    """
    is_payload, payload = decode_jwt(jwt_token, entity=entity)
    payload =  payload[0]
    token = payload["token"]
    if entity.lower() != 'admin':
        if all:
            xauth_models.AuthToken.objects.filter(user_id=payload["sub"]).delete()
        else:
            xauth_models.AuthToken.objects.filter(token=token).delete()
    else:
        if all:
            xauth_models.AdminAuthToken.objects.filter(user_id=payload["sub"]).delete()
        else:
            xauth_models.AdminAuthToken.objects.filter(token=token).delete()
