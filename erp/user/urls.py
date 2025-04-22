from django.urls import path

from user.views import TestView, LoginView, SaveView, PwdView, AvatarView, ImageView, SearchView, Actionview, Checkview
from user.views import JwtTestView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),  # 登录
    path('save', SaveView.as_view(), name='save'),  # 用户添加或者修改
    path('updateUserPwd', PwdView.as_view(), name='updateUserPwd'),  # 修改密码
    path('uploadImage', ImageView.as_view(), name='uploadImage'),  # 头像上传
    path('updateAvatar', AvatarView.as_view(), name='updateAvatar'),  # 更新头像
    path('search', SearchView.as_view(), name='search'),  # 用户信息查询

    path('action', Actionview.as_view(), name='action'),  # 用户信息操作
    path('check', Checkview.as_view(), name='check'),  # 用户名查重
    path('test', TestView.as_view(), name='test'),  # 测试
    path('jwt_test', JwtTestView.as_view(), name='jwt_test'),  # jwt测试
]
