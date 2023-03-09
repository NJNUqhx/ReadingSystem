from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        info_dict = request.session.get("info")
        if info_dict:
            return
        else:
            if "stu" in request.path_info:
                return redirect("/stu/login/")
            else:
                return redirect("/tec/login/")
