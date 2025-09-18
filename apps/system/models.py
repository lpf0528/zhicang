from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.models import BaseModel


class InvoiceInfo(BaseModel):
    title = models.CharField(max_length=255, verbose_name='单据标题')
    address = models.CharField(max_length=500, verbose_name='单据地址')
    telephone = models.CharField(max_length=255, verbose_name='单据电话(多个；)')
    remark = models.CharField(max_length=500, verbose_name='备注', null=True, blank=True)
    tip = models.CharField(max_length=500, verbose_name='提示',
                           default='温馨提示：请细查货物，如有质量问题请在七天内提出，一经开剪，恕不退换，谢谢合作。')

    class Meta:
        db_table = 'invoice_info'
        verbose_name = '单据信息'
        verbose_name_plural = '单据信息'


class CategoryConfig(BaseModel):
    class TypeChoices(models.TextChoices):
        # 客户
        CUSTOMER = 'customer', '客户：省内/省外'
        # 供应商
        SUPPLIER = 'supplier', '供应商：织厂/批发商'

    type = models.CharField(max_length=255, verbose_name='系统配置类型', choices=TypeChoices.choices)
    name = models.CharField(max_length=255, verbose_name='类别名称')
    remark = models.CharField(max_length=255, verbose_name='备注', null=True, blank=True)

    class Meta:
        db_table = 'category_config'
        verbose_name = '类别配置'
        verbose_name_plural = '类别配置'


class SystemConfig(BaseModel):
    class TypeChoices(models.TextChoices):
        PRODUCT_CATEGORY = 'product_category', '货物类别：布/纱/书版'
        UNIT = 'unit', '货物单位：米/本/套'
        VERSION = 'version', '版本：W03/W05'
        SETTLEMENT_METHOD = 'settlement_method', '结算方式：现金/月结/微信'
        LOGISTIC = 'logistic', '货运部：顺丰/拼包/申通/圆通'
        PAYMENT_METHOD = 'payment_method', '收款方式：现金/微信/支付宝'

    type = models.CharField(max_length=255, verbose_name='系统配置类型', choices=TypeChoices.choices)
    name = models.CharField(max_length=255, verbose_name='系统配置名称')
    remark = models.CharField(max_length=255, verbose_name='备注', null=True, blank=True)

    class Meta:
        db_table = 'system_config'
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'


# 部门
class Department(BaseModel):
    name = models.CharField(max_length=255, verbose_name='部门名称')
    remark = models.CharField(max_length=255, verbose_name='备注', null=True, blank=True)
    manager = models.ForeignKey('ZcUser', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='负责人',
                                related_name='department_manager')
    # 部门下的用户
    users = models.ManyToManyField('ZcUser', verbose_name='部门下的用户', related_name='department_users')

    class Meta:
        db_table = 'department'
        verbose_name = '部门'
        verbose_name_plural = '部门'


class ZcUser(AbstractUser):
    auth_code = models.CharField(max_length=255, verbose_name='授权码', null=True, blank=True)

    @staticmethod
    def get_tokens_for_user(user):
        if not user.is_active:
            raise AuthenticationFailed("无效用户，无法登录")

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
