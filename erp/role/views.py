import json
from datetime import datetime
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View

from menu.models import SysRoleMenu
from role.models import SysRole, SysRoleSerializer, SysUserRole


# Create your views here.
class ListAllView(View):
    def get(self, request):
        obj_roleList = SysRole.objects.all().values()
        roleList = list(obj_roleList)
        return JsonResponse({'code': 200, 'roleList': roleList})


# 角色信息查询
class SearchView(View):
    def post(self, request):
        # 使用 request.GET 获取查询字符串中的数据
        data = dict(request.GET)
        # request.GET 返回的是一个 QueryDict 对象，其中的值是列表形式，需要将其转换为单个值
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        pageNum = int(data['pageNum'])  # 当前页
        pageSize = int(data['pageSize'])  # 每页大小
        query = data['query']  # 查询参数

        # 过滤查询结果
        queryset = SysRole.objects.filter(name__icontains=query)
        # 对查询集进行排序
        queryset = queryset.order_by('id')  # 按照 id 字段进行排序
        # 创建分页器
        paginator = Paginator(queryset, pageSize)

        # 检查页码的有效性
        if pageNum > paginator.num_pages:
            pageNum = paginator.num_pages
        elif pageNum < 1:
            pageNum = 1

        # 获取指定页码的数据
        roleListPage = paginator.page(pageNum)

        obj_roles = roleListPage.object_list.values()  # 转成字典
        roles = list(obj_roles)  # 把外层的容器转为List
        total = queryset.count()

        return JsonResponse({'code': 200, 'roleList': roles, 'total': total})


class SaveView(View):
    def post(self, request):
        # 使用 request.GET 获取查询字符串中的数据
        data = dict(request.GET)
        # request.GET 返回的是一个 QueryDict 对象，其中的值是列表形式，需要将其转换为单个值
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        if data['id'] == '-1':  # 添加
            print('这里是role的添加')
            obj_sysRole = SysRole(name=data['name'], code=data['code'], remark=data['remark'])
            obj_sysRole.create_time = datetime.now().date()
            obj_sysRole.update_time = datetime.now().date()
            obj_sysRole.login_date = datetime.now().date()
            obj_sysRole.save()  # 添加
        else:  # 修改
            print('这里是role的修改')
            obj_sysRole = SysRole(id=data['id'], name=data['name'], code=data['code'],
                                  remark=data['remark'], create_time=data['create_time'],
                                  update_time=data['update_time'])
            obj_sysRole.update_time = datetime.now().date()
            obj_sysRole.save()
        return JsonResponse({'code': 200})


# 角色基本操作
class ActionView(View):
    def get(self, request):
        """
        根据id获取角色信息
        :param request:
        :return:
        """
        id = request.GET.get("id")
        role_object = SysRole.objects.get(id=id)
        return JsonResponse({'code': 200, 'role': SysRoleSerializer(role_object).data})

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

        SysUserRole.objects.filter(role_id__in=id_list).delete()
        SysRoleMenu.objects.filter(role_id__in=id_list).delete()
        SysRole.objects.filter(id__in=id_list).delete()
        return JsonResponse({'code': 200})


# 根据角色查询菜单权限
class MenusView(View):
    def get(self, request):
        id = request.GET.get("id")
        menuList = SysRoleMenu.objects.filter(role_id=id).values("menu_id")
        menuIdList = [m['menu_id'] for m in menuList]
        print("menuIdList=", menuIdList)
        return JsonResponse(
            {'code': 200, 'menuIdList': menuIdList})


# 角色权限授权
class GrantMenu(View):
    def post(self, request):
        # 使用 request.GET 获取查询字符串中的数据
        data = dict(request.GET)
        # request.GET 返回的是一个 QueryDict 对象，其中的值是列表形式，需要将其转换为单个值
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        role_id = data['id']
        menuIdList = data['menuIds[]']
        SysRoleMenu.objects.filter(role_id=role_id).delete()  # 删除角色菜单关联表中的指定角色数据
        for menuId in menuIdList:
            roleMenu = SysRoleMenu(role_id=role_id, menu_id=menuId)
            roleMenu.save()
        return JsonResponse({'code': 200})
