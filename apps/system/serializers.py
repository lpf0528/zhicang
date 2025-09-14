from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from system.models import ZcUser


# class ZcTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         # Add custom claims
#         token['username'] = user.username
#
#         return token


class ZcRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=False, label='用户名')
    password = serializers.CharField(max_length=100, required=False, label='密码')
    auth_code = serializers.CharField(max_length=100, required=False, label='授权码')

    def validate_username(self, value):
        if ZcUser.objects.filter(username=value).exists():
            raise serializers.ValidationError('用户名已存在')
        return value

    def validate_auth_code(self, value):
        if ZcUser.objects.filter(auth_code=value).exists():
            raise serializers.ValidationError('授权码已存在')
        return value

    def create(self, validated_data):
        user = ZcUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        tokens = ZcUser.get_tokens_for_user(user)
        return {
            'username': user.username,
            'refresh': tokens['refresh'],
            'access': tokens['access'],
        }
