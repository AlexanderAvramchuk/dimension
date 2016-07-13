# -*- coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver
from push_notifications.models import GCMDevice, APNSDevice
from datetime import datetime
WEEKDAY = timezone.now().weekday() + 1
DAY_OF_THE_WEEK = {
    '1': _(u'Monday'),
    '2': _(u'Tuesday'),
    '3': _(u'Wednesday'),
    '4': _(u'Thursday'),
    '5': _(u'Friday'),
    '6': _(u'Saturday'),
    '7': _(u'Sunday'),
}


class DayOfTheWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(DAY_OF_THE_WEEK.items()))
        kwargs['max_length'] = 1
        super(DayOfTheWeekField, self).__init__(*args, **kwargs)


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    en_image = models.ImageField(upload_to='images/', blank=True, null=True)
    de_image = models.ImageField(upload_to='images/', blank=True, null=True)
    payment = models.BooleanField(default=True)
    download_count = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Изображения"
        ordering = ['payment']


class Notification(models.Model):
    text = models.CharField(max_length=500)
    en_text = models.CharField(max_length=500, blank=True, default="")
    de_text = models.CharField(max_length=500, blank=True, default="")
    time = models.ForeignKey('api.Hour', related_name='notifications')
    cyclic = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    date = models.DateField(default=timezone.now().date())

    class Meta:
        verbose_name_plural = "Оповещения"

    def __unicode__(self):
        return self.text


class Hour(models.Model):
    time = models.TimeField()

    def __unicode__(self):
        return str(self.time)


class Push(models.Model):
    user = models.ForeignKey(User, related_name='pushes')
    notification = models.ForeignKey(Notification, related_name='pushes')
#    hour = models.ForeignKey('api.Hour', related_name='pushes')
    datetime = models.DateTimeField(null=True,blank=True)
    sound = models.CharField(max_length=50, default="alert.wav")
    def __unicode__(self):
        return str(self.notification.id)

    @property
    def date(self):
        return self.notification.date



@receiver(signals.post_save, sender=Notification)
def sync_notification(sender, instance, **kwargs):
    users = User.objects.all()
    for user in users:
        hour = instance.time
        d = datetime.combine(instance.date, instance.time.time)
        push = Push.objects.create(notification=instance, user=user, datetime=d)
        push.save()


@receiver(signals.post_save, sender=User)
def sync_user(sender, instance, **kwargs):
    notifications = Notification.objects.all()
    for notification in notifications:
        d = datetime.combine(notification.date, notification.time.time)
        push = Push.objects.filter(notification=notification, user=instance, datetime=d).first()
        if push:
            pass
        else:
            push  = Push.objects.create(notification=notification, user=instance, datetime=d)
            push.save()


#@receiver(signals.post_save, sender=APNSDevice)
#def create_user(sender, instance, **kwargs):
#    user = User.objects.create(username=instance.device_id)
#    user.save()
#    instance.user = user
#    instance.save()


@receiver(signals.post_save, sender=GCMDevice)
def create_user(sender, instance, **kwargs):
    user = User.objects.create(username=instance.device_id)
    user.save()
    instance.user = user
    instance.save()
