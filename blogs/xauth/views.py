from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from xuser import models as user_models
from xauth import serializers as xauth_serializers
from xauth import utils as xauth_utils

from xauth.responses import xauth_responses

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from xauth import models as xauth_models
from django.utils import timezone
import datetime

class JWTAuth(APIView):
    
    @permission_classes((AllowAny,))
    def post(self, request, *args, **kwargs):

        platform = "API"
        entity = request.headers.get('entity', None)
        if entity is None:
            return Response(data=xauth_responses.jwtautherror(message="Oops! The entity header cannot be blank"), status=status.HTTP_400_BAD_REQUEST)
        
        serialized_data = xauth_serializers.JWTAuthSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)

        try:
            user = xauth_utils.find_user(username=serialized_data.validated_data.get("username", None), entity=entity)
        except Exception as e:
            return Response(data=xauth_responses.jwtautherror(), status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(serialized_data.validated_data.get("password")):

            jwt_token = xauth_utils.create_jwt_token(user=user, platform=platform, entity=entity)

            # token_filter = {"user":f"{user.id}", "platform":f"{platform}"}
            # user_tokens = xauth_models.AuthToken.objects.filter(**token_filter)
            # if len(user_tokens) == 0:
            #     jwt_token = xauth_utils.encode_jwt(user, platform=platform)          
            # else:
            #     curr_token = user_tokens[0]
            #     if curr_token.expiry_date >= timezone.now():
            #         curr_token.expiry_date =  timezone.now() + datetime.timedelta(hours=72)
            #         curr_token.save()
            #         jwt_token = xauth_utils.regenerate_jwt(user=user, hours=72, platform=platform, token=curr_token.token)

            #     if curr_token.expiry_date < timezone.now():
            #         curr_token.delete()
            #         jwt_token = xauth_utils.encode_jwt(user, platform=platform)
            user.last_login = timezone.now()
            user.save()
            return Response(
                data=xauth_responses.jwtauthsuccess(jwt_token),
                status=status.HTTP_200_OK
            )
        else:
            return Response(data=xauth_responses.jwtautherror(), status=status.HTTP_401_UNAUTHORIZED)


class JWTDestroy(APIView):
    def get(self, request, *args, **kwargs):
        jwt_token = request.META.get("HTTP_AUTHORIZATION", "")
        entity = request.headers.get('entity', None)
        if entity is None:
            return Response(data=xauth_responses.jwtautherror(message="Oops! The entity header cannot be blank"), status=status.HTTP_400_BAD_REQUEST)
        try:
            jwt, is_all = jwt_token.split(" ", 1)[1], bool(request.query_params.get("all", False))
            xauth_utils.destroy_jwt(jwt, is_all, entity=entity)
        except Exception as e:
            return Response(data=xauth_responses.jwtautherror(message='User already logged out'), status=status.HTTP_400_BAD_REQUEST)
        return Response(data=xauth_responses.jwtlogoutsuccess(), status=status.HTTP_200_OK)
