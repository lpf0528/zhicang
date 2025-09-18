from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from common.response import result
from system.models import InvoiceInfo
from system.serializers import ZcRegisterSerializer, ZcLoginSerializer, InvoiceInfoModelSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, mixins, views


class ZcRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        ser = ZcRegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.create(ser.validated_data)
        return result.success(data=data, message='注册成功', response_status=status.HTTP_201_CREATED)


class ZcLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        ser = ZcLoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        return result.success(data=data)


class InvoiceInfoView(APIView):

    def get(self, request):
        invoice_info = InvoiceInfo.objects.filter(auth_code=request.user.auth_code).first()

        return result.success(InvoiceInfoModelSerializer(invoice_info).data)

    def post(self, request):
        if InvoiceInfo.objects.filter(auth_code=request.user.auth_code).exists():
            return result.error('发票详情已存在')
        ser = InvoiceInfoModelSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(auth_code=request.user.auth_code)
        return result.success()

    def patch(self, request):
        invoice_info = InvoiceInfo.objects.filter(auth_code=request.user.auth_code).first()
        if not invoice_info:
            return result.error('发票详情不存在')
        ser = InvoiceInfoModelSerializer(invoice_info, data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return result.success()
