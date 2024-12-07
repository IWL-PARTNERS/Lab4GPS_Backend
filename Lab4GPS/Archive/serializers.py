from rest_framework import serializers
from .models import Category, Tag, File, Comment, Like
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User details.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for file categories.
    """
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for tags associated with files.
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for user comments on files.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'file', 'user', 'text', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for tracking likes on files.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'file', 'user']


class FileSerializer(serializers.ModelSerializer):
    """
    Serializer for files in the archive.
    """
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    downloads_count = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = [
            'id',
            'title',
            'description',
            'category',
            'tags',
            'author',
            'upload_date',
            'version',
            'file',
            'media',
            'views_count',
            'downloads_count',
            'likes_count',
            'comments',
        ]

    def get_likes_count(self, obj):
        """
        Get the number of likes for a file.
        """
        return obj.likes.count()

    def get_downloads_count(self, obj):
        """
        Get the number of downloads for a file.
        """
        return obj.downloads

    def get_views_count(self, obj):
        """
        Get the number of views for a file.
        """
        return obj.views
