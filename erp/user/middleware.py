from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from rest_framework_jwt.settings import api_settings


# token验证中间件
class JwtAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        white_list = ["/user/login"]  # 请求白名单路径
        path = request.path  # 获取请求路径
        if path not in white_list and not path.startswith("/media"):  # 静态文件，图片等
            print("要进行token验证")
            token = request.META.get("HTTP_AUTHORIZATION")  # 获取到token
            try:
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER  # 解析token方法
                jwt_decode_handler(token)
            except ExpiredSignatureError:
                return HttpResponse("Token过期,请重新登录！")
            except InvalidTokenError:
                return HttpResponse("Token验证失败！")
            except PyJWTError:
                return HttpResponse("Token验证异常！")
        else:
            return None
