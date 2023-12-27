from django.http import JsonResponse
from rest_framework.views import APIView
from CustomAdmin.custom_permissions import IsAdminUser, IsSuperAdminUser
from CustomAdmin.services import CreateUserService, ListAllUserService, SubscriptionService, UserService
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class AdminCreateUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdminUser]

    def get(self, request, *args, **kwargs):
        return JsonResponse({"msg": "Wacto-Clone Service is running successfully."})

    def post(self, request, *args, **kwargs):
        return CreateUserService(request=request).post_view()


class AdminUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    def get(self, request, *args, **kwargs):
        return UserService(request=request, kwargs=kwargs).get_view()

    def post(self, request, *args, **kwargs):
        return UserService(request=request, kwargs=kwargs).post_view()

class AllSubscriptionView(APIView):
    def get(self, request, *args, **kwargs):
        return SubscriptionService(request=request, kwargs=kwargs).get_all_subscription_view()

    def post(self, request, *args, **kwargs):
        return SubscriptionService(request=request, kwargs=kwargs).add_new_subscription()

class SubscriptionView(APIView):
    def get(self, request, *args, **kwargs):
        return SubscriptionService(request=request, kwargs=kwargs).get_subscription_view()
   
    def put(self, request, *args, **kwargs):
        return SubscriptionService(request=request, kwargs=kwargs).update_subscription_view()


class ListAllUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser] 

    def get(self, request, *args, **kwargs):
        return ListAllUserService(request=request, kwargs=kwargs).get_all_users()