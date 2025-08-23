from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'post', 'author', 'created_at', 'updated_at')

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comments_count')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at', 'comments')
    
    def get_comments_count(self, obj):
        return obj.comments.count()

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content')