from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.core.mail import send_mail
from datetime import datetime

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create user and generate OTP
        user = CustomUser.objects.create_user(**validated_data)
        user.generate_otp()  # Generate OTP for email verification

        # Send OTP to user's email
        send_mail(
            'Your OTP for Lab4GPS',
            f'Your OTP is: {user.otp}',
            'Lab4GPS <lab4gps@gmail.com>',
            [user.email],
            fail_silently=False,
        )
        return user


class VerifyOtpSerializer(serializers.Serializer):
    """
    Serializer for verifying the OTP sent to the user's email.
    """
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
            if user.is_otp_expired():
                raise serializers.ValidationError("OTP has expired.")
            if user.otp != data['otp']:
                raise serializers.ValidationError("Invalid OTP.")
            user.is_verified = True
            user.clear_otp()
            return user
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")


class LoginSerializer(serializers.Serializer):
    """
    Serializer for logging in a user.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
            if not user.check_password(data['password']):
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_verified:
                raise serializers.ValidationError("Email not verified. Please verify your account.")
            return user
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user details.
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_verified')


class TokenSerializer(serializers.Serializer):
    """
    Serializer for generating JWT tokens.
    """
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for initiating forgot password flow by sending OTP.
    """
    email = serializers.EmailField()

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
            user.generate_reset_password_otp()

            # Send OTP to user's email
            send_mail(
                'Reset Your Password - Lab4GPS',
                f'Your OTP is: {user.reset_password_otp}',
                'Lab4GPS <lab4gps@gmail.com>',
                [user.email],
                fail_silently=False,
            )
            return user
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")


class VerifyResetOtpSerializer(serializers.Serializer):
    """
    Serializer for verifying the OTP sent for password reset.
    """
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
            if user.is_reset_password_otp_expired():
                raise serializers.ValidationError("OTP has expired.")
            if user.reset_password_otp != data['otp']:
                raise serializers.ValidationError("Invalid OTP.")
            user.clear_reset_password_otp()
            return user
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for resetting the user's password.
    """
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
            user.set_password(data['new_password'])
            user.save()
            return user
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")
