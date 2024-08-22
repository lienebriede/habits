from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        upload_to='images/', default='../ftpfkey8ogd3f06e0vle', blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"

# Signal handler function, profile automatically created when a user is created
def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(owner=instance)

# Connect to the signal
post_save.connect(create_profile, sender=User)

