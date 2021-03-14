from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from hotel_swagger import views

# 路由
router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet, base_name='user')
# router.register(r'groups', views.GroupViewSet, base_name='group')


router.register('city_info', views.City_infoSet, base_name='city_info')
router.register('hotel_info', views.Hotel_infoSet, base_name='hotel_info')
router.register('room_type_info', views.Room_type_infoSet, base_name='room_type_info')
router.register('rate_type_info', views.Rate_type_infoSet, base_name='rate_type_info')
router.register('room_image_info', views.Room_image_infoSet, base_name='room_image_info')
router.register('rateplan_info', views.RatePlan_infoSet, base_name='rateplan_info')
router.register('hotel_nightlyrate_info', views.Hotel_NightlyRate_infoSet, base_name='hotel_nightlyrate_info')
router.register('hotel_bookingrule_info', views.Hotel_BookingRule_infoSet, base_name='hotel_bookingrule_info')
router.register('hotel_refundrule_info', views.Hotel_RefundRule_infoSet, base_name='hotel_refundrule_info')
router.register('hotel_promotion_info', views.Hotel_Promotion_infoSet, base_name='hotel_promotion_info')
router.register('price_model_info', views.Price_model_infoSet, base_name='price_model_info')
router.register('order_info', views.Order_infoSet, base_name='order_info')
# router.register('api', views.Api_create_record, base_name='api')

# 重要的是如下三行
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    # swagger接口文档路由
    url(r'^docs/', schema_view, name="docs"),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    # drf登录
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
