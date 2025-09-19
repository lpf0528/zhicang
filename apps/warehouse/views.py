from common.response import result
from rest_framework import mixins, viewsets

from common.viewsets import ZCViewSet
from warehouse.models import Warehouse
from warehouse.serializers import WarehouseSerializer


class WarehouseViewSet(ZCViewSet, mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = WarehouseSerializer
    queryset = Warehouse.objects

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return result.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return result.success()
