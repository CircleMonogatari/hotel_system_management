# Create your views here.
# 视图
import serializers as serializers
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from rest_framework import viewsets
# from hotel_swagger.serializer import UserSerializer, GroupSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from hotel_admin import models
from hotel_swagger import serializers

from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class City_infoSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    queryset = serializers.City_infoSerializer.Meta.model.objects.all()
    serializer_class = serializers.City_infoSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class Hotel_infoSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    queryset = serializers.Hotel_infoSerializer.Meta.model.objects.all()
    serializer_class = serializers.Hotel_infoSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class Room_type_infoSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    queryset = serializers.Room_type_infoSerializer.Meta.model.objects.all()
    serializer_class = serializers.Room_type_infoSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class Rate_type_infoSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    queryset = serializers.Rate_type_infoSerializer.Meta.model.objects.all()
    serializer_class = serializers.Rate_type_infoSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class Room_image_infoSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    queryset = serializers.Room_image_infoSerializer.Meta.model.objects.all()
    serializer_class = serializers.Room_image_infoSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class RatePlan_infoSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    queryset = serializers.RatePlan_infoSerializer.Meta.model.objects.all()
    serializer_class = serializers.RatePlan_infoSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class Hotel_NightlyRate_infoSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView,
                                viewsets.GenericViewSet):
    queryset = serializers.Hotel_NightlyRate_infoSerializer.Meta.model.objects.all()
    serializer_class = serializers.Hotel_NightlyRate_infoSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class Hotel_BookingRule_infoSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView,
                                viewsets.GenericViewSet):
    queryset = serializers.Hotel_BookingRule_infoSerializer.Meta.model.objects.all()
    serializer_class = serializers.Hotel_BookingRule_infoSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class Hotel_RefundRule_infoSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView,
                               viewsets.GenericViewSet):
    queryset = serializers.Hotel_RefundRule_infoSerializer.Meta.model.objects.all()
    serializer_class = serializers.Hotel_RefundRule_infoSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class Hotel_Promotion_infoSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView,
                              viewsets.GenericViewSet):
    queryset = serializers.Hotel_Promotion_infoSerializer.Meta.model.objects.all()
    serializer_class = serializers.Hotel_Promotion_infoSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class Price_model_infoSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    queryset = serializers.Price_model_infoSerializer.Meta.model.objects.all()
    serializer_class = serializers.Price_model_infoSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class Order_infoSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    queryset = serializers.Order_infoSerializer.Meta.model.objects.all()
    serializer_class = serializers.Order_infoSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

# class UserViewSet(viewsets.ModelViewSet):
#     '''查看，编辑用户的界面'''
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     '''查看，编辑组的界面'''
#     queryset = Group
#     serializer_class = GroupSerializer

# class Api_create_record(GenericAPIView):
#
#     def post(self, request, *args, **kwargs):
#         text = request.POST['text']
#         return HttpResponse(text)
#
#     serializers_class = serializers.PostTextSerialzer
#     permission_classes = (AllowAny,)