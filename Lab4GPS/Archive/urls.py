from django.urls import path
from .views import (
    FileUploadView,
    FileListView,
    FileDetailView,
    LikeFileView,
    CommentFileView,
    CategoryListView,
    TagListView,
    IncrementDownloadCountView,
)

urlpatterns = [
    # File-related endpoints
    path('files/upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', FileListView.as_view(), name='file-list'),
    path('files/<int:pk>/', FileDetailView.as_view(), name='file-detail'),
    path('files/<int:pk>/like/', LikeFileView.as_view(), name='file-like'),
    path('files/<int:pk>/comments/', CommentFileView.as_view(), name='file-comments'),
    path('files/<int:pk>/increment-download/', IncrementDownloadCountView.as_view(), name='increment-download'),

    # Category and Tag endpoints
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('tags/', TagListView.as_view(), name='tag-list'),
]
