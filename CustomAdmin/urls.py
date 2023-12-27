from django.urls import path
from CustomAdmin.views import AllSubscriptionView, AdminCreateUserView, ListAllUserView, SubscriptionView, AdminUserView

urlpatterns = [
    path('create-user/', AdminCreateUserView.as_view(), name='register_user'),
    path('users/',ListAllUserView.as_view(),name="list-users"),
    path('user/<int:id>', AdminUserView.as_view(), name='get_user'),
    path('subscription', AllSubscriptionView.as_view(), name='subscriptions'),
    path('subscription/<int:id>', SubscriptionView.as_view(), name='specific_subscription'),
]
