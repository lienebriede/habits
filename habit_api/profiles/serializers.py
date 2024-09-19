from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Follow

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'bio', 'is_private'
        ]

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.SlugRelatedField(slug_field='username', read_only=True)
    followed_user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    status = serializers.ChoiceField(choices=Follow.FOLLOW_STATUS_CHOICES, default=Follow.APPROVED)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed_user', 'status', 'created_at']