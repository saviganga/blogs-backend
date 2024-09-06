from rest_framework import serializers

from xuser import models as user_models
from xuser.responses import u_responses

from django.db.models import Q
from django.utils.translation import gettext_lazy as _




class RegisterCustomUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(
        label=_("Repeat Password"),
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
    )


    class Meta:
        model = user_models.CustomUser
        fields = [
            "id",
            "user_name",
            "password",
            "re_password"
        ]

        extra_kwargs = {

            "password": {
                "write_only": True
            },
            "error_messages": {
                "required": "The password field is required"
            },
            "user_name": {
                "error_messages": {
                    "required": "The username field is required"
                }
            }

        }

    def create(self, validated_data):

        # validate password from validated data

        password = validated_data.pop("password")
        re_password = validated_data.pop("re_password")

        if password != re_password:
            return False, u_responses.user_error_responses(message='Oops! password mismatch')
        
        # create the user
        user = user_models.CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return True, user

class ReadCustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_models.CustomUser
        exclude = ('password', 'groups', 'user_permissions', 'is_superuser')



class RegisterAdminUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(
        label=_("Repeat Password"),
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
    )


    class Meta:
        model = user_models.AdminUser
        fields = [
            "id",
            "user_name",
            "password",
            "re_password"
        ]

        extra_kwargs = {

            "password": {
                "write_only": True
            },
            "error_messages": {
                "required": "The password field is required"
            },
            "user_name": {
                "error_messages": {
                    "required": "The username field is required"
                }
            }

        }

    def create(self, validated_data):

        # validate password from validated data

        password = validated_data.pop("password")
        re_password = validated_data.pop("re_password")

        if password != re_password:
            return False, u_responses.user_error_responses(message='Oops! password mismatch')
        
        # create the user
        user = self.Meta.model.objects.create(**validated_data)
        user.is_staff = True
        user.set_password(password)
        user.save()

        return True, user

class ReadAdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_models.AdminUser
        exclude = ('password', 'groups', 'user_permissions', 'is_superuser')


class RegisterUserResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    