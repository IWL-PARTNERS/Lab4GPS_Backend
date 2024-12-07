from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Category, Tag, File, Comment, Like
from .serializers import FileSerializer, CommentSerializer, LikeSerializer, CategorySerializer, TagSerializer
from django.db.models import Count


class FileUploadView(APIView):
    """
    API View for uploading files to the archive.
    """
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handles file upload requests.
        """
        data = request.data.copy()
        data['author'] = request.user.id  # Automatically associate the logged-in user as the author

        serializer = FileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileListView(generics.ListAPIView):
    """
    API View for retrieving and filtering files.
    """
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter files based on query parameters.
        """
        queryset = File.objects.all()
        category = self.request.query_params.get('category')
        tags = self.request.query_params.getlist('tags')
        search = self.request.query_params.get('search')

        if category:
            queryset = queryset.filter(category__name__iexact=category)
        if tags:
            queryset = queryset.filter(tags__name__in=tags).distinct()
        if search:
            queryset = queryset.filter(
                title__icontains=search
            ) | queryset.filter(description__icontains=search)

        return queryset


class FileDetailView(APIView):
    """
    API View for retrieving, updating, and deleting individual files.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        """
        Retrieve a single file by ID and increment its view count.
        """
        file = get_object_or_404(File, pk=pk)
        file.increment_views()
        serializer = FileSerializer(file)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete a file if the user is the author or an administrator.
        """
        file = get_object_or_404(File, pk=pk)
        if file.author != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to delete this file."},
                status=status.HTTP_403_FORBIDDEN,
            )
        file.delete()
        return Response({"detail": "File deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class LikeFileView(APIView):
    """
    API View for liking a file.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        """
        Toggle like on a file.
        """
        file = get_object_or_404(File, pk=pk)
        like, created = Like.objects.get_or_create(file=file, user=request.user)
        if not created:
            like.delete()  # Unlike if already liked
            return Response({"detail": "File unliked."}, status=status.HTTP_200_OK)
        return Response({"detail": "File liked."}, status=status.HTTP_201_CREATED)


class CommentFileView(APIView):
    """
    API View for adding comments to a file.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        """
        Add a comment to a file.
        """
        file = get_object_or_404(File, pk=pk)
        data = request.data.copy()
        data['file'] = file.id
        data['user'] = request.user.id

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(generics.ListAPIView):
    """
    API View for listing all categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class TagListView(generics.ListAPIView):
    """
    API View for listing all tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class IncrementDownloadCountView(APIView):
    """
    API View to increment the download count of a file.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        """
        Increment the download count for a file.
        """
        file = get_object_or_404(File, pk=pk)
        file.increment_downloads()
        return Response({"detail": "Download count incremented."}, status=status.HTTP_200_OK)
