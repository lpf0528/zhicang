from django.db import models
from django.contrib.auth.models import AnonymousUser

from common.middleware import CurrentUserMiddleware


class AuthCodeManager(models.Manager):
    def get_queryset(self):
        current_user = CurrentUserMiddleware.get_current_user()
        if current_user and not isinstance(current_user, AnonymousUser):
            return super().get_queryset().filter(auth_code=current_user.auth_code)
        else:
            return super().get_queryset().filter(auth_code=None)
