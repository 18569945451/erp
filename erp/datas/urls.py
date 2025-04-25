from django.urls import path
from datas.views import TransportRecordView

urlpatterns = [
    # 这里可以添加具体的路由规则
    path('transportRecord/', TransportRecordView.as_view(), name='transportRecord'),  # 获取运输记录数据
    path('pull/', TransportRecordView.as_view(), name='pull'),  # 获取运输记录数据
]
