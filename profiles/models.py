from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField  # Optional – used for thumbnailing

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

#class Profile(models.Model):
#    user = models.OneToOneField(
 #       User,
  #      on_delete=models.CASCADE,
   #     related_name="profile"
    #)
#    profile_image = models.ImageField(
 #       upload_to='profile_images/',
  #      null=True,
   #     blank=True,
    #)

    # Remove this if you're already using `profile_image` as the main field
    # image = ImageField(upload_to='profiles')  ← Not needed

# Automatically create a profile when new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
