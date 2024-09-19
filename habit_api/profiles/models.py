from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner.username}'s profile"

# Signal to automatically create a profile whenever a new user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(owner=instance)

# Signal to save the profile whenever the user is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Follow(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    DECLINED = 'declined'

    FOLLOW_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DECLINED, 'Declined'),
    ]

    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='following'
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='followers'
    )
    status = models.CharField(
        max_length=10, 
        choices=FOLLOW_STATUS_CHOICES, 
        default=APPROVED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed_user')

    def is_approved(self):
        return self.status == self.APPROVED

