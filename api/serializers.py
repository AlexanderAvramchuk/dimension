from models import Image, Notification, Hour, Push
from rest_framework import serializers
from push_notifications.models import APNSDevice, GCMDevice
from models import User


class ImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'image', 'en_image', 'de_image', 'download_count', 'payment', )


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    time = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ('id', 'text', 'en_text', 'de_text', 'date', 'time', 'cyclic', 'active', )


class APNSDeviceSerializer(serializers.HyperlinkedRelatedField):
    class Meta:
        model = APNSDevice
        fields = ('id', 'name', 'active', 'user', 'device_id', 'registration_id', )


class GCMDeviceSerializer(serializers.HyperlinkedRelatedField):
    class Meta:
        model = GCMDevice
        fields = ('id', 'name', 'active', 'user', 'device_id', 'registration_id', )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)


class HourSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hour
        fields = ('id', 'time',)


class PushSerializer(serializers.HyperlinkedModelSerializer):
    notification = serializers.StringRelatedField()

    class Meta:
        model = Push
        fields = ('id', 'user', 'notification', 'datetime', 'date', 'sound')





