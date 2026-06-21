from django.db.models.signals import post_save
from django.dispatch import receiver
from followers.models import Follower
from .models import Notification

@receiver(post_save, sender=Follower)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.following,
            sender=instance.followed_by,
            notification_type='follow',
            message=f'started following you'
        )
