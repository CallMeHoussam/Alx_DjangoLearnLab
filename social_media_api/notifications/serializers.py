from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserNotificationSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'actor', 'verb', 'target_object_id', 
                 'message', 'is_read', 'created_at')
        read_only_fields = ('id', 'recipient', 'actor', 'verb', 'target_object_id', 
                          'message', 'created_at')

class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('is_read',)