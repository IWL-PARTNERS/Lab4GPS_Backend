# problem/serializers.py

from rest_framework import serializers
from Auths.models import CustomUser
from .models import Problem, MediaFile

class MediaFileSerializer(serializers.ModelSerializer):
    """
    Serializer for MediaFile model to handle media uploads and retrievals.
    """
    class Meta:
        model = MediaFile
        fields = ['id', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

class ProblemSerializer(serializers.ModelSerializer):
    """
    Serializer for the Problem model, now including nested MediaFile uploads.
    """
    submitter = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True
    )
    media_files = MediaFileSerializer(many=True, read_only=True)
    media_files_upload = serializers.ListField(
        child=serializers.FileField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
        help_text="List of media files (images, videos) to upload."
    )

    class Meta:
        model = Problem
        fields = [
            "id",
            "submitter",
            "problem_title",
            "description",
            "category",
            "urgency",
            "country",
            "city",
            "latitude",
            "longitude",
            "media_files",
            "media_files_upload",
            "submitter_photo",
            "contact_name",
            "contact_email",
            "contact_phone",
            "date_created",
        ]
        read_only_fields = ("id", "date_created", "media_files")

    def create(self, validated_data):
        """
        Override create method to handle media file uploads.
        """
        media_files = validated_data.pop('media_files_upload', [])
        problem = Problem.objects.create(**validated_data)
        for file in media_files:
            MediaFile.objects.create(problem=problem, file=file)
        return problem

    def to_representation(self, instance):
        """
        Customize the representation to include URLs for media files and submitter photo.
        """
        representation = super().to_representation(instance)
        # Add submitter_photo URL if exists
        if instance.submitter_photo:
            representation['submitter_photo_url'] = instance.submitter_photo.url
        else:
            representation['submitter_photo_url'] = None
        # Add media_files URLs
        representation['media_files_urls'] = [media.file.url for media in instance.media_files.all()]
        return representation
