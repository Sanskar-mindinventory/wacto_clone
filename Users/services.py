from datetime import datetime, timedelta, timezone
import os
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
import pytz
import requests
from Users.constants import ACCOUNT_DOESNT_EXIST, COMPANY_ADDED, COMPANY_DETAIL_DOES_NOT_EXIST, COMPANY_DETAIL_UPDATED, COMPANY_DOES_NOT_EXIST, EMAIL_IS_NOT_VERIFIED, EMAIL_SENT_SUCCESSFULLY, EMAIL_VERIFICATION_LINK_SHARED, MESSAGE_TEMPLATE, MOBILE_NUMBER_VERIFIED, NETTYFISH_MESSAGE_SEND_URL, OTP_SHARED_SUCCESSFULLY, PASSWORD_CHANGED_SUCCESSFULLY, RESET_PASSWORD_EMAIL_SENT, SOMETHING_WENT_WRONG, SUBSCRIPTION_ADDED, SUBSCRIPTION_DOES_NOT_EXIST, SUBSCRIPTION_UPDATED, USER_CREATED, USER_DOES_NOT_EXIST, USER_EXISTS, USER_UPDATED, YOU_CAN_NOT_UPDATE
from Users.models import CompanyDetails, CustomUser, DropDownCategoryItem, Subscription
from Users.serializers import ChangePasswordSerializer, CompanyDetailSerializer, DropDownCategoryItemSerializer, EmailSerializer, ForgotPasswordSerializer, OTPSerializer, SubscriptionSerializer, UserSerializer
from django.utils.http import urlsafe_base64_decode

from Users.utils.common_utils import CommonUtils, OTPGeneration, SendVerificationEmail

class CreateUserService:
    def __init__(self, request):
        self.request = request

    def post_view(self):
        data = self.request.data
        serialized_user = UserSerializer(data=data, context={'request':self.request})
        if serialized_user.is_valid():
            user = serialized_user.save()
            SendVerificationEmail.send_verification_email(request_site=self.request, user=user)
            msg = USER_CREATED.format(email=user.email)
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
            user_serialized = UserSerializer(user_instance, context={'request':self.request})
            return JsonResponse(user_serialized.data, status=200, safe=False)
        return JsonResponse({"msg": USER_DOES_NOT_EXIST.format(id=self.kwargs.get('id'))}, status=400, safe=False)

    def post_view(self):
        data = self.request.data
        user_instance = CustomUser.get_user(
            kwargs={"id": self.kwargs.get('id')})
        if not user_instance:
            return JsonResponse({"msg": USER_DOES_NOT_EXIST.format(id=self.kwargs.get('id')) + YOU_CAN_NOT_UPDATE}, status=400, safe=False)
        serialized_user = UserSerializer(
            instance=user_instance, data=data, partial=True, context={'request':self.request})
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
                return JsonResponse({'msg':USER_EXISTS}, status=200)
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
        return JsonResponse({'msg':ACCOUNT_DOESNT_EXIST}, status=200)
    
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


class ListAllUserService:
    def __init__(self, request, kwargs):
        self.request = request
        self.kwargs = kwargs

    def get_all_users(self):
        users = CustomUser.get_user()
        users_data = UserSerializer(users, many=True, context={'request':self.request})
        return JsonResponse(users_data.data, status=200, safe=False)
    

class MobileOTPService:
    def __init__(self, request, kwargs):
        self.request = request
        self.kwargs = kwargs

    def send_otp(self):
        generated_otp = OTPGeneration.create_otp(n=4)
        user = CustomUser.get_user(kwargs={"id":self.request.user.id})
        json_payload = {
            "senderId": os.getenv("SENDER_ID"),
            "message": MESSAGE_TEMPLATE.format(minutes=os.getenv('OTP_EXPIRY_TIME','5'),generated_otp=generated_otp),
            "mobileNumbers": user.mobile_number,
            "templateId": os.getenv("TEMPLATE_ID"),
            "apiKey": os.getenv("NETTYFISH_API_KEY"),
            "clientId": os.getenv("NETTYFISH_CLIENT_ID")            
        }
        response = requests.post(url=NETTYFISH_MESSAGE_SEND_URL, json=json_payload)
        current_time = datetime.now(timezone.utc).replace(tzinfo=pytz.utc)
        otp_expiry_time = (datetime.strptime(current_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
                                                     '%Y-%m-%d %H:%M:%S.%f') + timedelta(minutes=int(os.getenv('OTP_EXPIRY_TIME','5')))).replace(
                    tzinfo=pytz.utc)
        user = CustomUser.update_user(user_id=self.request.user.id,kwargs={'otp':generated_otp, 'otp_expiry_time':otp_expiry_time})
        return JsonResponse({'msg': OTP_SHARED_SUCCESSFULLY.format(mobile=f"{user.country_code}-{user.mobile_number}")},status=200)

    def verify_otp(self):
        data  = self.request.data 
        user = CustomUser.get_user(kwargs={"id":self.request.user.id})
        otp_data = OTPSerializer(instance=user, data=data, context={"request":self.request})
        if otp_data.is_valid():
            otp_data.save()
            return JsonResponse({'msg':MOBILE_NUMBER_VERIFIED}, status=200)
        return JsonResponse(otp_data.errors, status=400)


class CategoryService:
    def __init__(self, request, kwargs):
        self.request = request
        self.kwargs = kwargs
   
    def get_category_view(self):
        category_items = DropDownCategoryItem.get_category_items(kwargs={"category_id": self.kwargs.get('category_id')})
        serializer = DropDownCategoryItemSerializer(category_items, many=True)
        return JsonResponse(serializer.data, safe=False)

    
class CompanyDetailService:
    def __init__(self, request, kwargs):
        self.request = request
        self.kwargs = kwargs

    def get_all_company_detail_view(self):
        company_detail = CompanyDetails.get_company_detail()
        serializer = CompanyDetailSerializer(company_detail, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def get_company_detail_view(self):
        company_detail = CompanyDetails.get_company_detail(kwargs={"id": self.kwargs.get('id')})
        serializer = CompanyDetailSerializer(company_detail)
        if serializer:
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse({"msg": COMPANY_DETAIL_DOES_NOT_EXIST.format(id=self.kwargs.get('id'))}, status=400, safe=False)
    
    def add_new_company_detail_view(self):
        data = self.request.data
        data['user']=self.request.user.id
        serialized_company_detail = CompanyDetailSerializer(data=data)
        if serialized_company_detail.is_valid():
            company_detail = serialized_company_detail.save()
            msg = COMPANY_ADDED.format(id=company_detail.id)
            return JsonResponse({"msg": msg, 'data': serialized_company_detail.data}, status=201)
        return JsonResponse(serialized_company_detail.errors, status=400)

    def update_company_detail_view(self):
        data = self.request.data
        company_detail_instance = CompanyDetails.get_company_detail(
            kwargs={"id": self.kwargs.get('id')})
        if not company_detail_instance:
            return JsonResponse({"msg": COMPANY_DOES_NOT_EXIST.format(id=self.kwargs.get('id')) + YOU_CAN_NOT_UPDATE}, status=400, safe=False)
        serialized_company_detail = CompanyDetailSerializer(
            instance=company_detail_instance, data=data, partial=True)
        if serialized_company_detail.is_valid():
            company_detail = serialized_company_detail.save()
            msg = COMPANY_DETAIL_UPDATED.format(id=company_detail.id)
            return JsonResponse({"msg": msg, 'data': serialized_company_detail.data}, status=200)
        return JsonResponse(serialized_company_detail.errors, status=400)