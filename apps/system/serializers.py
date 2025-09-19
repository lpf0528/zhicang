from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from common.exception.app_exception import AppApiException
from system.models import ZcUser, InvoiceInfo, SystemConfig


class ZcRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, required=True, label='用户名',
                                     error_messages={'max_length': '用户名长度不能超过20位',
                                                     'required': '用户名是必填的'})
    password = serializers.CharField(max_length=50, required=True, label='密码',
                                     error_messages={'max_length': '密码长度不能超过30位',
                                                     'required': '密码是必填的'})
    auth_code = serializers.CharField(max_length=9, min_length=9, required=False, label='授权码',
                                      error_messages={'max_length': '请输入9位授权码',
                                                      'min_length': '请输入9位授权码'})

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


class ZcLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, required=True, label='用户名',
                                     error_messages={'max_length': '用户名长度不能超过20位',
                                                     'required': '用户名是必填的'})
    password = serializers.CharField(max_length=50, required=True, label='密码',
                                     error_messages={'max_length': '密码长度不能超过30位',
                                                     'required': '密码是必填的'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = ZcUser.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError('用户名不存在')
        if not user.check_password(password):
            raise serializers.ValidationError('密码错误')
        tokens = ZcUser.get_tokens_for_user(user)
        return {
            'refresh': tokens['refresh'],
            'access': tokens['access'],
        }


class InvoiceInfoSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, required=True, label='单据标题',
                                  error_messages={'required': '单据标题是必填的'})
    address = serializers.CharField(max_length=500, required=True, label='单据地址',
                                    error_messages={'required': '单据地址是必填的'})
    telephone = serializers.CharField(max_length=255, required=True, label='单据电话(多个；)',
                                      error_messages={'required': '单据电话是必填的'})
    remark = serializers.CharField(max_length=500, required=True, label='备注',
                                   error_messages={'required': '备注是必填的'})
    tip = serializers.CharField(max_length=255, required=False, label='备注')

    class Meta:
        model = InvoiceInfo
        fields = ('id', 'title', 'address', 'telephone', 'remark', 'tip')
        exclude = ['auth_code']

    def save(self, **kwargs):
        auth_code = kwargs.get('auth_code')
        obj, _ = InvoiceInfo.objects.update_or_create(auth_code=auth_code,
                                                      defaults=self.validated_data)
        return obj


class SystemConfigSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=SystemConfig.TypeChoices.choices, required=True, label='配置类型',
                                   error_messages={'required': '配置类型是必填的',
                                                   'invalid_choice': '“{input}”配置类型选择错误'})

    value = serializers.CharField(max_length=255, required=True, label='配置值',
                                  error_messages={'required': '配置值是必填的'})
    remark = serializers.CharField(max_length=255, required=False, label='备注')

    def save(self, **kwargs):
        auth_code = kwargs.get('auth_code')
        obj, _ = SystemConfig.objects.update_or_create(auth_code=auth_code, type=self.validated_data['type'],
                                                       defaults={'value': self.validated_data['value'],
                                                                 'remark': self.validated_data.get('remark', '')})
        return obj

    class Meta:
        model = SystemConfig
        fields = ('type', 'value', 'remark')
        exclude = ['auth_code']
