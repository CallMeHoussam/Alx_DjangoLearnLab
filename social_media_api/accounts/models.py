from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following_users')
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followed_by')
    
    # Add custom related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    
    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Follow another user"""
        if user != self and user not in self.following.all():
            self.following.add(user)
            user.followers.add(self)
            return True
        return False
    
    def unfollow(self, user):
        """Unfollow another user"""
        if user in self.following.all():
            self.following.remove(user)
            user.followers.remove(self)
            return True
        return False
    
    def is_following(self, user):
        """Check if following a user"""
        return self.following.filter(id=user.id).exists()