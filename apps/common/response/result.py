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


def success(data=None, **kwargs):
    """
    获取一个成功的响应对象
    :param data: 接口响应数据
    :return: 请求响应对象
    """
    return Result(data=data, **kwargs)


def error(message, **kwargs):
    """
    获取一个失败的响应对象
    :param message: 错误提示
    :return: 接口响应对象
    """
    return Result(code=500, message=message, **kwargs)
