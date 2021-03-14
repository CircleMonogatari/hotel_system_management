# 序列化
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from hotel_admin import models


class City_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City_info
        fields = '__all__'


class Hotel_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotel_info
        fields = '__all__'


class Room_type_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room_type_info
        fields = '__all__'


class Rate_type_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rate_type_info
        fields = '__all__'


class Room_image_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room_image_info
        fields = '__all__'


class RatePlan_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RatePlan_info
        fields = '__all__'


class Hotel_NightlyRate_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotel_NightlyRate_info
        fields = '__all__'


class Hotel_BookingRule_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotel_BookingRule_info
        fields = '__all__'


class Hotel_RefundRule_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotel_RefundRule_info
        fields = '__all__'


class Hotel_Promotion_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotel_Promotion_info
        fields = '__all__'


class Price_model_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Price_model_info
        fields = '__all__'


class Order_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order_info
        fields = '__all__'


#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"
#
#
# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = "__all__"


# class PostTextSerialzer(serializers.Serializer):
#     # 参数字段，通过设定不同的参数可以出现不同的组合效果，可以具体参照django文档
#     text = serializers.CharField()

    # class Meta:
    #     fields = "__all__"
