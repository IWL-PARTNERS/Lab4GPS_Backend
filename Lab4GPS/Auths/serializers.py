from rest_framework import serializers
from .models import CustomUser
from django.core.mail import send_mail


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


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating user profile details.
    """
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'profile_picture', 'is_verified', 'registration_date')
        read_only_fields = ('is_verified', 'registration_date', 'profile_picture')


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user details (excluding password and profile picture).
    """
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username')

    def update(self, instance, validated_data):
        instance.update_profile(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            username=validated_data.get('username'),
        )
        return instance


class UpdateProfilePictureSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the user's profile picture.
    """
    profile_picture = serializers.ImageField()

    class Meta:
        model = CustomUser
        fields = ('profile_picture',)

    def update(self, instance, validated_data):
        instance.update_profile_picture(validated_data.get('profile_picture'))
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing the user's password.
    """
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError("Old password is incorrect.")
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    """
    Serializer for generating JWT tokens.
    """
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


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
