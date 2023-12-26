from django.http import JsonResponse
from rest_framework.views import APIView

from Users.services import CreateUserService, SubscriptionService, UserService


class CreateUserView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"msg": "Wacto-Clone Service is running successfully.   "})

    def post(self, request, *args, **kwargs):
        return CreateUserService(request=request).post_view()


class UserView(APIView):
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
