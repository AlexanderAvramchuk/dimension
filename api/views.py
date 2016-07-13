# -*- coding: utf-8
from models import Image, Notification, Push, Hour
from serializers import ImageSerializer, NotificationSerializer, UserSerializer, HourSerializer, PushSerializer
from django.utils import timezone
from datetime import timedelta
from pagination import  StandardResultsSetPagination
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet, GCMDeviceAuthorizedViewSet
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from push_notifications.models import APNSDevice, GCMDevice

class APNSViewSet(APNSDeviceAuthorizedViewSet):
    permission_classes = [AllowAny,]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class HourViewSet(viewsets.ModelViewSet):
    queryset = Hour.objects.all()
    serializer_class = HourSerializer


class PushViewSet(viewsets.ModelViewSet):
    queryset = Push.objects.all()
    serializer_class = PushSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('user', 'notification')


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    pagination_class = StandardResultsSetPagination


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


@api_view(['POST'])
def create_notification(request):
    response_dict = dict()
    if request.method == 'POST':
        data = request.data
        object = Notification.objects.create()
        for key, value in data.iteritems():
            setattr(object, key, value)
        object.save()
        response_dict['message'] = u"Оповещение успешно создано"
    return Response(response_dict)


@api_view(['POST'])
def update_push(request):
    response_dict = dict()
    if request.method == 'POST':
        data = request.data
        
        push = Push.objects.filter(id=data['id']).first()
        if data['datetime']:
            push.datetime = data['datetime']
        push.save()
        response_dict['status'] = True
        response_dict['message'] = u'Успешно отредактировано'
    return Response(response_dict)


@api_view(['POST'])
def delete_push(request):
    response_dict = dict()
    if request.method == 'POST':
        data = request.data
        try:
            push = Push.objects.get(id=data['id'])
            push.delete()
            response_dict['status'] = True
            response_dict['message'] = u'Пуш удален'
        except Push.DoesNotExist:
            response_dict['status'] = True
            response_dict['message'] = u'Не существует пуша'
    return Response(response_dict)




@api_view(['POST'])
def delete_notification(request):
    response_dict = dict()
    if request.method == 'POST':
        data = request.data
        object = Notification.objects.filter(id=data['id']).first()
        if object:
            object.delete()
            response_dict['message'] = u"Оповещение успешно удалено"
        else:
            response_dict['message'] = u"Оповещение не найдено"
    return Response(response_dict)


@api_view(['POST'])
def register_apns(request):
    response_dict = dict()
    data = request.data
    
    device = APNSDevice.objects.filter(registration_id=data['registration_id'], device_id=data['device_id']).first()
    if device:
        response_dict['message'] = "This device is already registered"
    else:      
        device = APNSDevice.objects.create(name=data['name'],
                                           registration_id=data['registration_id'],
                                           device_id=data['device_id'],
                                           active=data['active'])
        try:
            user = User.objects.get(username=device.device_id)
        except User.DoesNotExist:
            user = User.objects.create(username=device.device_id)
            user.save()
            device.user = user
            device.save()

            response_dict['user_id'] = device.user.id
    return Response(response_dict)





@api_view(['POST'])
def increment_download_count(request):
    response_dict = dict()
    image = Image.objects.get(id=request.data['id'])
    image.download_count += 1
    image.save()
    response_dict['status'] = True
    return Response(response_dict)
