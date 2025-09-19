from rest_framework import serializers
from django.db import connection

from warehouse.models import Warehouse


class WarehouseSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Warehouse
        exclude = ['auth_code']

    def save(self, **kwargs):
        # if 'id' in self.initial_data:
        obj, _ = Warehouse.objects.update_or_create(id=self.initial_data.get('id'),
                                                    defaults=self.validated_data)
        return obj
