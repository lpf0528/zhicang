from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from common.response import result
from system.models import InvoiceInfo, SystemConfig
from system.serializers import ZcRegisterSerializer, ZcLoginSerializer, InvoiceInfoSerializer, \
    SystemConfigSerializer

from rest_framework import status


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
        invoice_info = InvoiceInfo.objects.filter().first()

        return result.success(InvoiceInfoSerializer(invoice_info).data)

    def post(self, request):
        ser = InvoiceInfoSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(auth_code=request.user.auth_code)
        return result.success()


class SystemConfigView(APIView):
    def get(self, request):
        instances = SystemConfig.objects.filter().all()
        ser = SystemConfigSerializer(instances, many=True)
        return result.success(data=ser.data)

    def post(self, request):
        ser = SystemConfigSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        ser.save(auth_code=request.user.auth_code)
        return result.success()
