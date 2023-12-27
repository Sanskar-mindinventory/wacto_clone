from multiprocessing import context
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from Users.constants import EMAIL_IS_NOT_VERIFIED, EMAIL_SENT_SUCCESSFULLY, EMAIL_VERIFICATION_LINK_SHARED, PASSWORD_CHANGED_SUCCESSFULLY, RESET_PASSWORD_EMAIL_SENT, SOMETHING_WENT_WRONG, SUBSCRIPTION_ADDED, SUBSCRIPTION_DOES_NOT_EXIST, SUBSCRIPTION_UPDATED, USER_CREATED, USER_DOES_NOT_EXIST, USER_EXISTS, USER_UPDATED, YOU_CAN_NOT_UPDATE
from Users.models import CustomUser, Subscription
from Users.serializers import ChangePasswordSerializer, EmailSerializer, ForgotPasswordSerializer, SubscriptionSerializer, UserSerializer
from django.utils.http import urlsafe_base64_decode

from Users.utils.common_utils import CommonUtils, SendVerificationEmail

class CreateUserService:
    def __init__(self, request):
        self.request = request

    def post_view(self):
        data = self.request.data
        serialized_user = UserSerializer(data=data)
        if serialized_user.is_valid():
            user = serialized_user.save()
            SendVerificationEmail.send_verification_email(request_site=self.request, user=user)
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
    

class SendVerificationEmailService:
    def __init__(self, request, kwargs):
        self.request = request
        self.kwargs = kwargs

    def check_email_availability(self):
        data = self.request.data
        user = CustomUser.get_user(kwargs={'email':data.get('email')})
        redirect_uri = '/signup'
        if user:
            if user.is_email_verified:
                return JsonResponse({'msg':USER_EXISTS.format(username=user.email)}, status=200)
            else:
                email = EmailSerializer(data=data)
                if email.is_valid():
                    SendVerificationEmail.send_verification_email(request_site=self.request, user=user)
                return JsonResponse({'msg':EMAIL_VERIFICATION_LINK_SHARED.format(email=user.email)}, status=400)
        return JsonResponse({'msg':'Success', 'redirect_uri':redirect_uri}, status=200)

    def verify_email_view(self):
        user_email_base_64 = self.kwargs.get('uidb64')
        user_token = self.kwargs.get('token')
        email = urlsafe_base64_decode(user_email_base_64).decode('utf-8')
        user = CustomUser.get_user(kwargs={'email':email})
        if self.validate_token(token=user_token, user=user):
            user.is_email_verified = True
            user.save()
            return JsonResponse({'msg': "Email is verified successfully"}, status=200)
        else:
            return JsonResponse({'msg': 'Verification link is expired'}, status=400)
    
    def validate_token(self, user, token):
        token_generator = default_token_generator
        is_not_expired = token_generator.check_token(user=user, token=token)
        return is_not_expired


class ResetPasswordService:
    def __init__(self, request, kwargs):
        self.request = request
        self.kwargs = kwargs

    def send_reset_password_email(self):
        data = self.request.data
        email = EmailSerializer(data=data)
        user = CustomUser.get_user(kwargs={'email':data.get('email')})
        if user and email.is_valid():
            SendVerificationEmail.send_reset_password_email(request_site=self.request, user=user)
            return JsonResponse({'msg':RESET_PASSWORD_EMAIL_SENT}, status=200)
        return JsonResponse({'msg':EMAIL_IS_NOT_VERIFIED}, status=200)
    
    def change_forgotted_password(self):
        data = self.request.data
        user_email_base_64 = self.kwargs.get('uidb64')
        # Need to add user token validation.
        user_token = self.kwargs.get('token')
        email = urlsafe_base64_decode(user_email_base_64).decode('utf-8')
        user = CustomUser.get_user(kwargs={"email":email})
        password = ForgotPasswordSerializer(instance=user, data=data)
        if password.is_valid():
            password.save()
            return JsonResponse({"msg":PASSWORD_CHANGED_SUCCESSFULLY}, status=200)
        return JsonResponse(password.errors, status=400)
    
    
class ChangePasswordService:
    def __init__(self, request, kwargs):
        self.request =request
        self.kwargs = kwargs

    def change_password(self):
        data = self.request.data    
        user = CustomUser.get_user(kwargs={"id": data.get('id')})
        password = ChangePasswordSerializer(instance=user, data=data, context={'request':self.request})
        if password.is_valid():
            password.save()
            return JsonResponse({"msg":PASSWORD_CHANGED_SUCCESSFULLY}, status=200)
        return JsonResponse(password.errors, status=400)
