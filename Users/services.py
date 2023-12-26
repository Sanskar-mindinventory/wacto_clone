from django.http import JsonResponse
from Users.constants import SUBSCRIPTION_ADDED, SUBSCRIPTION_DOES_NOT_EXIST, SUBSCRIPTION_UPDATED, USER_CREATED, USER_DOES_NOT_EXIST, USER_UPDATED, YOU_CAN_NOT_UPDATE
from Users.models import CustomUser, Subscription
from Users.serializers import SubscriptionSerializer, UserSerializer


class CreateUserService:
    def __init__(self, request):
        self.request = request

    def post_view(self):
        data = self.request.data
        serialized_user = UserSerializer(data=data)
        if serialized_user.is_valid():
            user = serialized_user.save()
            msg = USER_CREATED.format(username=user.username, id=user.id)
            return JsonResponse({"msg": msg, 'data': serialized_user.data}, status=201)
        return JsonResponse(serialized_user.errors, status=400)


class UserService:
    def __init__(self, request, kwargs):
        self.request = request
        self.kwargs = kwargs

    def get_view(self):
        user_instance = CustomUser.get_user(
            kwargs={"id": self.kwargs.get('id')})
        if user_instance:
            user_serialized = UserSerializer(user_instance)
            return JsonResponse(user_serialized.data, status=200, safe=False)
        return JsonResponse({"msg": USER_DOES_NOT_EXIST.format(id=self.kwargs.get('id'))}, status=400, safe=False)

    def post_view(self):
        data = self.request.data
        user_instance = CustomUser.get_user(
            kwargs={"id": self.kwargs.get('id')})
        if not user_instance:
            return JsonResponse({"msg": USER_DOES_NOT_EXIST.format(id=self.kwargs.get('id')) + YOU_CAN_NOT_UPDATE}, status=400, safe=False)
        serialized_user = UserSerializer(
            instance=user_instance, data=data, partial=True)
        if serialized_user.is_valid():
            user = serialized_user.save()
            msg = USER_UPDATED.format(username=user.username)
            return JsonResponse({"msg": msg, 'data': serialized_user.data}, status=200)
        return JsonResponse(serialized_user.errors, status=400)
    

class SubscriptionService:

    def __init__(self, request, kwargs):
        self.request = request
        self.kwargs = kwargs

    def get_all_subscription_view(self):
        subscriptions = Subscription.get_subscription()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def get_subscription_view(self):
        subscriptions = Subscription.get_subscription(kwargs={"id": self.kwargs.get('id')})
        serializer = SubscriptionSerializer(subscriptions)
        return JsonResponse(serializer.data, safe=False)
    
    def add_new_subscription(self):
        data = self.request.data
        serialized_subscription = SubscriptionSerializer(data=data)
        if serialized_subscription.is_valid():
            subscription = serialized_subscription.save()
            msg = SUBSCRIPTION_ADDED.format(id=subscription.id)
            return JsonResponse({"msg": msg, 'data': serialized_subscription.data}, status=201)
        return JsonResponse(serialized_subscription.errors, status=400)

    def update_subscription_view(self):

        data = self.request.data
        subscription_instance = Subscription.get_subscription(
            kwargs={"id": self.kwargs.get('id')})
        if not subscription_instance:
            return JsonResponse({"msg": SUBSCRIPTION_DOES_NOT_EXIST.format(id=self.kwargs.get('id')) + YOU_CAN_NOT_UPDATE}, status=400, safe=False)
        serialized_subscription = SubscriptionSerializer(
            instance=subscription_instance, data=data, partial=True)
        if serialized_subscription.is_valid():
            subscription = serialized_subscription.save()
            msg = SUBSCRIPTION_UPDATED.format(id=subscription.id)
            return JsonResponse({"msg": msg, 'data': serialized_subscription.data}, status=200)
        return JsonResponse(serialized_subscription.errors, status=400)
