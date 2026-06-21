from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):

    last_seen = models.DateTimeField(auto_now=True)
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
    )
    cover_photo = models.ImageField(
        upload_to='cover_photos/',
        null=True,
        blank=True,
    )
    def __str__(self):
        return self.user.username

    # Remove this if you're already using `profile_image` as the main field
    # image = ImageField(upload_to='profiles')  ← Not needed

# Automatically create a profile when new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
