from django.contrib import admin
from .models import Category, Tag, File, Comment, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing categories.
    """
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin interface for managing tags.
    """
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    """
    Admin interface for managing files in the archive.
    """
    list_display = ('id', 'title', 'category', 'author', 'upload_date', 'views', 'downloads')
    list_filter = ('category', 'author', 'upload_date')
    search_fields = ('title', 'description')
    autocomplete_fields = ('category', 'author', 'tags')
    readonly_fields = ('views', 'downloads')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'tags', 'author', 'version')
        }),
        ('File Details', {
            'fields': ('file', 'media', 'views', 'downloads')
        }),
        ('Dates', {
            'fields': ('upload_date',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface for managing comments on files.
    """
    list_display = ('id', 'file', 'user', 'text', 'created_at')
    list_filter = ('file', 'user', 'created_at')
    search_fields = ('text', 'user__username', 'file__title')
    ordering = ('-created_at',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing likes on files.
    """
    list_display = ('id', 'file', 'user')
    list_filter = ('file', 'user')
    search_fields = ('user__username', 'file__title')
