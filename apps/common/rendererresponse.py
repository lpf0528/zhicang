from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:

            # 如果返回的data为字典
            if isinstance(data, dict):
                msg = data.pop('message', '请求成功')
                code = data.pop('code', renderer_context["response"].status_code)
            else:
                msg = '请求成功'
                code = renderer_context["response"].status_code

            # 自定义返回的格式
            ret = {
                'msg': msg,
                'code': code,
                'data': data.pop('data', {}),
            }
            # 返回JSON数据
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
