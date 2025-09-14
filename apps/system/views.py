from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from system.serializers import ZcRegisterSerializer

from rest_framework import status
from rest_framework.response import Response


class ZcRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        ser = ZcRegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.create(ser.validated_data)
        return Response({'message': '注册成功', 'data': data}, status=status.HTTP_201_CREATED)
