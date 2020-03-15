from django.http import HttpResponse


class BlockIpMiddleware(object):
    """中间件类"""
    excludes_ip = ['127.0.0.2', 'other_ips']

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        """定义中间件实例方法"""
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in BlockIpMiddleware.excludes_ip:
            return HttpResponse('您无权访问次网站')
