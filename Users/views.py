from django.http import JsonResponse
from rest_framework.views import APIView

from Users.services import ChangePasswordService, CreateUserService, ResetPasswordService, SubscriptionService, UserService, SendVerificationEmailService

class CheckEmailAvailabilityView(APIView):
    def post(self, request, *args, **kwargs):
        return SendVerificationEmailService(request=request, kwargs=kwargs).check_email_availability()


class EmailVerificationView(APIView):
    def get(self, request, *args, **kwargs):
        return SendVerificationEmailService(request=request, kwargs=kwargs).verify_email_view()


class CreateUserView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"msg": "Wacto-Clone Service is running successfully."})

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
    
class ResetPasswordView(APIView):   
    def post(self, request, *args, **kwargs):
        return ResetPasswordService(request=request, kwargs=kwargs).send_reset_password_email()
    

class ResetPasswordConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        return ResetPasswordService(request=request, kwargs=kwargs).change_forgotted_password()
    

class ChangePasswordView(APIView):
    def post(self,request, *args, **kwargs):
        return ChangePasswordService(request=request, kwargs=kwargs).change_password()