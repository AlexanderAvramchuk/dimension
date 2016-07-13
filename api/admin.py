# -*- coding: utf-8
from django.contrib import admin
from models import Image, Notification, Hour, Push


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'en_image', 'de_image')

    class Meta:
        model = Image

admin.site.register(Image, ImageAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('text','date', 'time', 'cyclic', 'active', )
    class Meta:
        model = Notification

admin.site.register(Notification, NotificationAdmin)


class HourAdmin(admin.ModelAdmin):
    list_display = ('id', 'time',)

    class Meta:
        model = Hour

admin.site.register(Hour, HourAdmin)


class PushAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime', )

    class Meta:
        model = Push

admin.site.register(Push, PushAdmin)
