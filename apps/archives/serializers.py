from random import choices
import string
from archives.models import Supplier, Customer

from rest_framework import serializers


class SupplierSerializer(serializers.ModelSerializer):
    number = serializers.CharField(required=False, min_length=15, max_length=15)

    class Meta:
        model = Supplier
        exclude = ['auth_code']

    def validate(self, attrs):
        if 'number' not in attrs or not attrs['number'] or not Supplier.objects.filter(number=attrs['number']).exists():
            attrs['number'] = ''.join(choices(string.ascii_uppercase + string.digits, k=15))
            while Supplier.objects.filter(number=attrs['number']).exists():
                attrs['number'] = ''.join(choices(string.ascii_uppercase + string.digits, k=15))

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        number = self.validated_data.pop('number')
        obj, _ = Supplier.objects.update_or_create(auth_code=user.auth_code, number=number,
                                                   defaults=self.validated_data)
        return obj


class CustomerSerializer(serializers.ModelSerializer):
    number = serializers.CharField(required=False, min_length=15, max_length=15)

    class Meta:
        model = Customer
        exclude = ['auth_code']

    def validate(self, attrs):
        if 'number' not in attrs or not attrs['number'] or not Customer.objects.filter(number=attrs['number']).exists():
            attrs['number'] = ''.join(choices(string.ascii_uppercase + string.digits, k=15))
            while Customer.objects.filter(number=attrs['number']).exists():
                attrs['number'] = ''.join(choices(string.ascii_uppercase + string.digits, k=15))

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        number = self.validated_data.pop('number')
        obj, _ = Customer.objects.update_or_create(auth_code=user.auth_code, number=number,
                                                   defaults=self.validated_data)
        return obj
