from django.db import models


class BaseModel(models.Model):
    auth_code = models.CharField(max_length=255, verbose_name='授权码', null=True, blank=True)
    create_user_id = models.CharField(max_length=255, verbose_name='创建用户ID', null=True, blank=True)
    update_user_id = models.CharField(max_length=255, verbose_name='更新用户ID', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 动态发布时间
    updated_at = models.DateTimeField(auto_now=True)  # 动态更新时间
    is_delete = models.BooleanField(default=False, verbose_name="删除标记")

    class Meta:
        abstract = True
