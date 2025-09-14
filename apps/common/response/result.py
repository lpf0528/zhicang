from django.http import JsonResponse
from rest_framework import status


class Result(JsonResponse):
    charset = 'utf-8'
    """
     接口统一返回对象
    """

    def __init__(self, code=200, message='Success', data=None, response_status=status.HTTP_200_OK, **kwargs):
        back_info_dict = {"code": code, "message": message, 'data': data}
        super().__init__(data=back_info_dict, status=response_status, **kwargs)
