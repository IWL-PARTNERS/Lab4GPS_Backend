from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone  # Use Django's timezone utilities
from datetime import timedelta
import random


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.
    Adds fields for email verification and OTP functionality.
    """
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)  # Status of email verification
    otp = models.CharField(max_length=6, blank=True, null=True)  # OTP for verification
    otp_created_at = models.DateTimeField(blank=True, null=True)  # Timestamp for OTP creation
    reset_password_otp = models.CharField(max_length=6, blank=True, null=True)  # OTP for password reset
    reset_password_otp_created_at = models.DateTimeField(blank=True, null=True)  # Timestamp for reset OTP creation

    def __str__(self):
        return self.username

    def generate_otp(self):
        """
        Generate a random 6-digit OTP for email verification.
        """
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()  # Use timezone-aware datetime
        self.save()

    def clear_otp(self):
        """
        Clear the email verification OTP after verification.
        """
        self.otp = None
        self.otp_created_at = None
        self.save()

    def is_otp_expired(self):
        """
        Check if the email verification OTP is expired.
        """
        if self.otp_created_at:
            expiry_time = self.otp_created_at + timedelta(minutes=10)  # OTP valid for 10 minutes
            return timezone.now() > expiry_time  # Use timezone-aware datetime
        return True

    def generate_reset_password_otp(self):
        """
        Generate a random 6-digit OTP for password reset.
        """
        self.reset_password_otp = str(random.randint(100000, 999999))
        self.reset_password_otp_created_at = timezone.now()  # Use timezone-aware datetime
        self.save()

    def clear_reset_password_otp(self):
        """
        Clear the password reset OTP after successful reset.
        """
        self.reset_password_otp = None
        self.reset_password_otp_created_at = None
        self.save()

    def is_reset_password_otp_expired(self):
        """
        Check if the password reset OTP is expired.
        """
        if self.reset_password_otp_created_at:
            expiry_time = self.reset_password_otp_created_at + timedelta(minutes=10)  # OTP valid for 10 minutes
            return timezone.now() > expiry_time  # Use timezone-aware datetime
        return True
