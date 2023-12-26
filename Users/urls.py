from django.urls import path
from Users.views import AllSubscriptionView, CreateUserView, EmailVerificationView, SubscriptionView, UserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='register_user'),
    path('user/<int:id>', UserView.as_view(), name='get_user'),
    path('subscription', AllSubscriptionView.as_view(), name='subscriptions'),
    path('subscription/<int:id>', SubscriptionView.as_view(), name='specific_subscription'),
    path('login/', TokenObtainPairView.as_view(), name='login_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('email-verification/<uidb64>/<token>/', EmailVerificationView.as_view(), name='verify-email')
]
