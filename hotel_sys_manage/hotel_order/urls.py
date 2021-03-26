from django.conf.urls import url
from hotel_order import views


urlpatterns = [
    # swagger接口文档路由

    url('order_created', views.Order_create.as_view(), name='order_created'),
    url('order_cancel', views.Order_cancel.as_view(), name='order_cancel'),

]
