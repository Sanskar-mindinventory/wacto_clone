from django.http import JsonResponse
from rest_framework.views import APIView
from Users.custom_permissions import IsAdminUser
from Users.services import CategoryService, ChangePasswordService, CompanyDetailService, CreateUserService, ListAllUserService, MobileOTPService, ResetPasswordService, SubscriptionService, UserService, SendVerificationEmailService
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


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
    
class ResetPasswordView(APIView):   
    def post(self, request, *args, **kwargs):
        return ResetPasswordService(request=request, kwargs=kwargs).send_reset_password_email()
    

class ResetPasswordConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        return ResetPasswordService(request=request, kwargs=kwargs).change_forgotted_password()
    

class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    def post(self,request, *args, **kwargs):
        return ChangePasswordService(request=request, kwargs=kwargs).change_password()
    

class ListAllUserView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminUser] 

    def get(self, request, *args, **kwargs):
        return ListAllUserService(request=request, kwargs=kwargs).get_all_users()


class SendMobileOTPView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return MobileOTPService(request=request, kwargs=kwargs).send_otp()


class VerifyMobileOTPView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return MobileOTPService(request=request, kwargs=kwargs).verify_otp()
    


class CategoryListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return CategoryService(request=request, kwargs=kwargs).get_category_view()
    



class AllCompanyDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return CompanyDetailService(request=request, kwargs=kwargs).get_all_company_detail_view()

    def post(self, request, *args, **kwargs):
        return CompanyDetailService(request=request, kwargs=kwargs).add_new_company_detail_view()

class CompanyDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return CompanyDetailService(request=request, kwargs=kwargs).get_company_detail_view()
   
    def put(self, request, *args, **kwargs):
        return CompanyDetailService(request=request, kwargs=kwargs).update_company_detail_view()