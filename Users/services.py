from django.contrib.auth.tokens import default_token_generator
from urllib import request
from django.http import JsonResponse
from Users.constants import EMAIL_SENT_SUCCESSFULLY, EMAIL_VERIFICATION_LINK_SHARED, SUBSCRIPTION_ADDED, SUBSCRIPTION_DOES_NOT_EXIST, SUBSCRIPTION_UPDATED, USER_CREATED, USER_DOES_NOT_EXIST, USER_EXISTS, USER_UPDATED, YOU_CAN_NOT_UPDATE
from Users.models import CustomUser, Subscription
from Users.serializers import EmailSerializer, SubscriptionSerializer, UserSerializer
from django.utils.http import urlsafe_base64_decode

from Users.utils.common_utils import CommonUtils
from Users.utils.email_utils import EmailUtils

class CreateUserService:
    def __init__(self, request):
        self.request = request

    def post_view(self):
        data = self.request.data
        serialized_user = UserSerializer(data=data)
        if serialized_user.is_valid():
            user = serialized_user.save()
            SendVerificationEmail.send_verification_email(request=self.request, user=user)
            msg = USER_CREATED.format(username=user.username, id=user.id)
            return JsonResponse({"msg": msg, 'data': serialized_user.data}, status=201)
        return JsonResponse(serialized_user.errors, status=400)


class SendVerificationEmail:
    @staticmethod
    def send_verification_email(request, user):
        context = CommonUtils(request=request).create_context(user=user)
        html_content = f'<a type="button" style="color: #0a3370;padding: 7px 15px; color: #fff; background: #0a3370; border-radius: 20px;text-decoration: none;display: inline-block;" href="{context.get("protocol")}://{context.get("domain")}/user-auth/email-verification/{context.get("uid")}/{context.get("token")}/">Verification Link</a>'
        EmailUtils().send_email(to_emails=user.email, subject='Testing Mail', html_content=html_content)


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
        # todo: Need to add Redirect routes for the login if company is already added.
        redirect_uri = '/signup'
        if user:
            if user.is_email_verified:
                redirect_uri='/companydetails'
                return JsonResponse({'msg':USER_EXISTS.format(username=user.email), 'redirect_uri':redirect_uri}, status=200)
            else:
                email = EmailSerializer(data=data)
                if email.is_valid():
                    SendVerificationEmail.send_verification_email(request=request, user=user)
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