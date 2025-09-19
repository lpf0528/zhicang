from common.models import BaseModel


class ZCViewSet:

    def get_queryset(self):
        return self.queryset.filter()
