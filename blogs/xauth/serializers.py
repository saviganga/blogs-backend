from rest_framework import serializers


class JWTAuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, error_messages={'required': 'Username field is required', 'blank': 'Username field cannot be blank' })
    password = serializers.CharField(required=True, error_messages={'required': 'Password field is required', 'blank': 'Password field cannot be blank' } )
