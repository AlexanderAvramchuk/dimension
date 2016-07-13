from django.conf.urls import url, include
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet, GCMDeviceAuthorizedViewSet
from rest_framework import routers
from views import *

router = routers.DefaultRouter()

router.register(r'images', ImageViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'device/apns', APNSViewSet)
router.register(r'device/gcm', GCMDeviceAuthorizedViewSet)
router.register(r'users', UserViewSet)
router.register(r'pushes', PushViewSet)
router.register(r'hours', HourViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^update_push', update_push),
    url(r'^register_apns', register_apns),
    url(r'^increment_download_count', increment_download_count),
    url(r'^delete_push/', delete_push),
]

