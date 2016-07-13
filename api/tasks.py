from celery import Celery
from dimension.celery import app
from models import Hour, Push, Notification
from django.utils import timezone
from push_notifications.models import APNSDevice, GCMDevice

def sendAPNS(hour):
    date = timezone.now().date()
    notification = Notification.objects.filter(time=hour, date=date).first()
    if notification:
        devices = APNSDevice.objects.filter(active=True).all()
        for device in devices:
            device.send_message(notification.text, extra={'aps':{'sound':'alert.wav', 'alert':notification.text}, 'message':notification.text, })
    return True


@app.task(name='push')
def push():
    now = timezone.now().hour
    hour = Hour.objects.filter(time__hour=now+3).first()
    s = sendAPNS(hour)
    return s
