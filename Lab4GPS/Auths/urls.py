from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    VerifyOtpView,
    LoginView,
    UserDetailView,
    ForgotPasswordView,
    VerifyResetOtpView,
    ResetPasswordView,
)

urlpatterns = [
    # Endpoint for user registration
    path('signup/', RegisterView.as_view(), name='signup'),

    # Endpoint for verifying the OTP
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),

    # Endpoint for user login
    path('login/', LoginView.as_view(), name='login'),

    # Endpoint for refreshing the access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Endpoint for retrieving authenticated user details
    path('user/', UserDetailView.as_view(), name='user_detail'),

    # Endpoint for forgot password
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),

    # Endpoint for verifying OTP for password reset
    path('verify-reset-otp/', VerifyResetOtpView.as_view(), name='verify_reset_otp'),

    # Endpoint for resetting the password
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
]
