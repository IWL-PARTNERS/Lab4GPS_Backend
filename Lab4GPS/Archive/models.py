from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    """
    Model for file categories.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Model for tags associated with files.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class File(models.Model):
    """
    Model representing a file in the archive.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="files"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="files")
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="files"
    )
    upload_date = models.DateTimeField(default=timezone.now)
    version = models.PositiveIntegerField(default=1)
    file = models.FileField(upload_to="archive_files/")
    media = models.URLField(
        max_length=500, blank=True, null=True, help_text="Optional image or video URL"
    )
    views = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def increment_views(self):
        """
        Increment the view count for the file.
        """
        self.views += 1
        self.save()

    def increment_downloads(self):
        """
        Increment the download count for the file.
        """
        self.downloads += 1
        self.save()


class Comment(models.Model):
    """
    Model for user comments on files.
    """
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.file.title}"


class Like(models.Model):
    """
    Model for tracking likes on files.
    """
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes"
    )

    class Meta:
        unique_together = ("file", "user")

    def __str__(self):
        return f"{self.user.username} liked {self.file.title}"
