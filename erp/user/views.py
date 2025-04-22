from datetime import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.context_processors import request
from django.views import View
from rest_framework_jwt.settings import api_settings
import json
from erp import settings

from menu.models import SysMenu, SysMenuSerializer
from role.models import SysRole, SysUserRole
from user.models import SysUser, SysUserSerializer


class LoginView(View):
    # 构建菜单树
    def buildTreeMenu(self, sysMenuList):
        resultMenuList: list[SysMenu] = list()
        for menu in sysMenuList:
            for e in sysMenuList:
                if e.parent_id == menu.id:
                    if not hasattr(menu, "children"):
                        menu.children = list()
                    menu.children.append(e)
            # 1.判断父节点创建集合，寻找子节点加入对应父节点
            if menu.parent_id == 0:
                resultMenuList.append(menu)
        return resultMenuList

    def post(self, request):
        username = request.GET.get('username')
        password = request.GET.get('password')
        try:
            user = SysUser.objects.get(username=username, password=password)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 荷载操作（内容）
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 编码操作
            # 将用户的对象传递进去，获取该对象的属性值
            payload = jwt_payload_handler(user)
            # 将属性值编码成jwt格式的字符串（生成jwt token）
            token = jwt_encode_handler(payload)
            # 获取身份权限信息
            roleList = SysRole.objects.raw(
                "SELECT id,name FROM sys_role WHERE id IN (SELECT role_id FROM sys_user_role WHERE user_id = " + str(
                    user.id) + ")")
            # 获取当前用户的所有角色，逗号隔开
            roles = ",".join([role.name for role in roleList])
            menuSet: set[SysMenu] = set()  # 实例化去重复类
            for row in roleList:  # 查询权限目录
                menuList = SysMenu.objects.raw(
                    "SELECT * FROM sys_menu WHERE id IN (SELECT menu_id FROM sys_role_menu WHERE role_id = " + str(
                        row.id) + ")")
                for row2 in menuList:
                    menuSet.add(row2)
            # print(menuSet)
            menuList: list[SysMenu] = list(menuSet)  # 把set转为list
            sorted_enusList = sorted(menuList)  # 根据order_num排序
            # print(sorted_enusList)
            # 构建菜单树
            sysMenuList: list[SysMenu] = self.buildTreeMenu(sorted_enusList)
            # print(sysMenuList)
            serializerMenuList = list()
            for sysMenu in sysMenuList:
                serializerMenuList.append(SysMenuSerializer(sysMenu).data)
                # print(serializerMenuList)
        except Exception as e:
            return JsonResponse({'code': 500, 'info': e})
        return JsonResponse({'code': 200, "user": SysUserSerializer(user).data, 'token': token, "info": '登录成功！',
                             'menuList': serializerMenuList, 'roles': roles})


# Create your views here.
class TestView(View):
    def get(self, request):
        UserList_obj = SysUser.objects.all()
        UserList_dict = UserList_obj.values()
        Userlist = list(UserList_dict)
        return JsonResponse({'code': 200, 'info': Userlist})


class JwtTestView(View):
    def get(self, request):
        user = SysUser.objects.get(username='python222', password='123456')
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 荷载操作（内容）
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 编码操作
        # 将用户的对象传递进去，获取该对象的属性值
        payload = jwt_payload_handler(user)
        # 将属性值编码成jwt格式的字符串（生成jwt token）
        token = jwt_encode_handler(payload)
        return JsonResponse({'code': 200, 'token': token})


class SaveView(View):
    def post(self, request):
        # 使用 request.GET 获取查询字符串中的数据
        data = dict(request.GET)
        # request.GET 返回的是一个 QueryDict 对象，其中的值是列表形式，需要将其转换为单个值
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        print(data['id'])
        if data['id'] == "-1":  # 添加
            print('我是-1里面的')
            obj_sysUser = SysUser(username=data['username'], password=data['password'],
                                  email=data['email'], phonenumber=data['phonenumber'],
                                  status=data['status'],
                                  remark=data['remark'])
            obj_sysUser.create_time = datetime.now().date()
            obj_sysUser.avatar = 'default.jpg'
            obj_sysUser.password = "123456"
            obj_sysUser.save()
        else:
            print('我是else里面的')
            obj_sysUser = SysUser(id=data['id'], username=data['username'], password=data['password'],
                                  avatar=data['avatar'], email=data['email'], phonenumber=data['phonenumber'],
                                  login_date=data['login_date'], status=data['status'], create_time=data['create_time'],
                                  update_time=data['update_time'], remark=data['remark'])
            obj_sysUser.update_time = datetime.now().date()
            obj_sysUser.save()
        return JsonResponse({'code': 200})


class PwdView(View):
    def post(self, request):
        # 使用 request.GET 获取查询字符串中的数据
        data = dict(request.GET)
        # request.GET 返回的是一个 QueryDict 对象，其中的值是列表形式，需要将其转换为单个值
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        print(data)
        id = data['id']
        oldPassword = data['oldPassword']
        newPassword = data['newPassword']

        try:
            obj_user = SysUser.objects.get(id=id)
            if obj_user.password == oldPassword:
                obj_user.password = newPassword
                obj_user.update_time = datetime.now()
                obj_user.save()
                return JsonResponse({'code': 200})
            else:
                return JsonResponse({'code': 500, 'errorInfo': '原密码错误!'})
        except SysUser.DoesNotExist:
            return JsonResponse({'code': 500, 'errorInfo': '用户不存在!'})


class ImageView(View):
    def post(self, request):
        file = request.FILES.get('avatar')
        print("file:", file)
        if file:
            file_name = file.name
            suffixName = file_name[file_name.rfind("."):]
            new_file_name = datetime.now().strftime('%Y%m%d%H%M%S') + suffixName
            file_path = str(settings.MEDIA_ROOT) + "\\userAvatar\\" + new_file_name
            print("file_path:", file_path)
            try:
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                return JsonResponse({'code': 200, 'title': new_file_name})
            except:
                return JsonResponse({'code': 500, 'errorInfo': '上传头像失败'})


class AvatarView(View):
    def post(self, request):
        # 使用 request.GET 获取查询字符串中的数据
        data = dict(request.GET)
        # request.GET 返回的是一个 QueryDict 对象，其中的值是列表形式，需要将其转换为单个值
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        id = data['id']
        avatar = data['avatar']
        obj_user = SysUser.objects.get(id=id)
        obj_user.avatar = avatar
        obj_user.save()
        return JsonResponse({'code': 200})


class SearchView(View):
    def post(self, request):
        # 使用 request.GET 获取查询字符串中的数据
        data = dict(request.GET)
        # request.GET 返回的是一个 QueryDict 对象，其中的值是列表形式，需要将其转换为单个值
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        pageNum = data['pageNum']  # 当前页
        pageSize = data['pageSize']  # 每页大小
        query = data['query']  # 查询参数
        print(pageNum, pageSize)
        userListPage = Paginator(SysUser.objects.filter(username__icontains=query), pageSize).page(pageNum)
        print(userListPage)
        obj_users = userListPage.object_list.values()  # 转成字典
        users = list(obj_users)  # 把外层的容器转为List
        for user in users:
            userId = user['id']
            roleList = SysRole.objects.raw(
                "SELECT id,name FROM sys_role WHERE id IN (SELECT role_id FROM sys_user_role WHERE user_id =" + str(
                    userId) + ")")
            roleListDict = []
            for role in roleList:
                roleDict = {}
                roleDict['id'] = role.id
                roleDict['name'] = role.name
                roleListDict.append(roleDict)
            user['roleList'] = roleListDict
        total = SysUser.objects.filter(username__icontains=query).count()
        return JsonResponse({'code': 200, 'userList': users, 'total': total})


class Actionview(View):
    def get(self, request):
        """
         根据id获取用户信息
         :param request:
         :return:
         """
        id = request.GET.get("id")
        user_object = SysUser.objects.get(id=id)
        return JsonResponse({'code': 200, 'user': SysUserSerializer(user_object).data})

    def delete(self, request):
        """
        删除操作
        :param request:
        :return:
        """
        # 使用 request.GET 获取查询字符串中的数据
        idList = dict(request.GET)
        # request.GET 返回的是一个 QueryDict 对象，其中的值是列表形式，需要将其转换为单个值
        for key, value in idList.items():
            if isinstance(value, list) and len(value) == 1:
                idList[key] = value[0]
        # 将字典的值转换为整数列表
        id_list = [int(id) for id in idList.values()]
        SysUserRole.objects.filter(user_id__in=id_list).delete()
        SysUser.objects.filter(id__in=id_list).delete()
        return JsonResponse({'code': 200})


class Checkview(View):
    def post(self, request):
        # 使用 request.GET 获取查询字符串中的数据
        data = dict(request.GET)
        # request.GET 返回的是一个 QueryDict 对象，其中的值是列表形式，需要将其转换为单个值
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        username = data['username']
        print("username=", username)
        if SysUser.objects.filter(username=username).exists():
            return JsonResponse({'code': 500})
        else:
            return JsonResponse({'code': 200})
