from django.db import models

from apps.common.models import BaseModel


class Supplier(BaseModel):
    number = models.CharField(max_length=15, unique=True, verbose_name='供应商编号')
    name = models.CharField(max_length=255, verbose_name='供应商名称')
    category = models.CharField(max_length=255, verbose_name='供应商类别(没有及新增)：织厂/批发商', null=True,
                                blank=True)
    contact_name = models.CharField(max_length=255, verbose_name='联系人姓名', null=True, blank=True)
    contact_phone = models.CharField(max_length=255, verbose_name='联系人手机号', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='供应商地址', null=True, blank=True)
    email = models.CharField(max_length=255, verbose_name='联系人邮箱', null=True, blank=True)
    remark = models.CharField(max_length=255, verbose_name='备注', null=True, blank=True)

    class Meta:
        db_table = 'supplier'
        verbose_name = '供应商'
        verbose_name_plural = '供应商'


class Customer(BaseModel):
    number = models.CharField(max_length=255, unique=True, verbose_name='客户编号')
    name = models.CharField(max_length=255, verbose_name='客户名称')
    category = models.CharField(max_length=255, verbose_name='客户类别:省内/省外', null=True, blank=True)
    contact_name = models.CharField(max_length=255, verbose_name='联系人姓名', null=True, blank=True)
    contact_phone = models.CharField(max_length=255, verbose_name='联系人手机号', null=True, blank=True)
    logistic = models.CharField(max_length=255, verbose_name='货运部', null=True, blank=True)
    province = models.CharField(max_length=255, verbose_name='省份', null=True, blank=True)
    city = models.CharField(max_length=255, verbose_name='城市', null=True, blank=True)
    street = models.CharField(max_length=255, verbose_name='街道', null=True, blank=True)
    remark = models.CharField(max_length=255, verbose_name='备注')

    class Meta:
        db_table = 'customer'
        verbose_name = '客户'
        verbose_name_plural = '客户'
