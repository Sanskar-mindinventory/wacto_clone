from django.urls import path
from Users.views import AllSubscriptionView, CreateUserView, EmailVerificationView, ListAllUserView, SubscriptionView, UserView, CheckEmailAvailabilityView, ResetPasswordView, ResetPasswordConfirmView, ChangePasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='register_user'),
    path('users/',ListAllUserView.as_view(),name="list-users"),
    path('user/<int:id>', UserView.as_view(), name='get_user'),
    path('subscription', AllSubscriptionView.as_view(), name='subscriptions'),
    path('subscription/<int:id>', SubscriptionView.as_view(), name='specific_subscription'),
    path('email-verification/<uidb64>/<token>/', EmailVerificationView.as_view(), name='verify_email'),
    path('check-email/', CheckEmailAvailabilityView.as_view(), name='check_email_availability'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password-confirm/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
    path('change-password/',ChangePasswordView.as_view(), name="change_password"),
    # JWT Authentication Views
    path('login/', TokenObtainPairView.as_view(), name='login_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
