from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import  HttpResponse,redirect


class AuthMiddleware(MiddlewareMixin):
    """中间件"""
    def process_request(self,request):
        #0 .排除那些不需要登录就可以访问的页面
        #request.path_info  获取当前用户请求的URL /login/
        if request.path_info in ["/login/",'/image/code/']:
            return

        #1.读取当前访问的用户的sesion信息，如果能读取到，说明可以继续执行
        info_dict = request.session.get("info")
        if info_dict:
            return

        # 2 .如果没有登录过
        return redirect('/login/')


        #如果方法中没有返回值，（返回None),继续执行
        #如果有返回值，HttpResponse，render,redirecit
        # print("M1.process_request")
        # return HttpResponse("无权访问")




    # def process_response(self,request,response):
    #     print("M1.process_response")



# class M2(MiddlewareMixin):
#     """中间件"""
#
#     def process_request(self, request):
#         print("M2.process_request")
#
#     def process_response(self, request, response):
#         print("M2.process_response")