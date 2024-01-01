from datetime import datetime, timezone
from django.contrib.auth.hashers import make_password, check_password
import pytz
from rest_framework import serializers
from Users.models import CompanyDetails, CustomUser, DropDownCategoryItem, Subscription
from Users.utils.common_utils import CommonUtils, SendVerificationEmail
from regex_validations import RegexValidation
from Users.constants import COMPANY_INDUSTRY_MISSING, COMPANY_NAME_PATTERN, COMPANY_PURPOSE_MISSING, COMPANY_SIZE_MISSING, COUNTRY_CODE_MISSING, EMAIL_PATTERN, EMAIL_VERIFICATION_LINK_SHARED, FIRST_NAME_PATTERN, INVALID_COMPANY_NAME, INVALID_COUNTRY_CODE, INVALID_CREDENTIALS, INVALID_EMAIL_FORMAT, INVALID_FIRST_NAME, INVALID_LAST_NAME, INVALID_MOBILE_NUMBER, INVALID_OTP, INVALID_PASSWORD_FORMAT, LAST_NAME_PATTERN, MOBILE_NUMBER_ALREADY_EXIST, MOBILE_NUMBER_PATTERN, OTP_IS_EXPIRED, PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH, PASSWORD_AND_OLD_PASSWORD_ARE_SAME, PASSWORD_PATTERN, SOURCE_ERROR, USER_DOES_NOT_EXIST, USERNAME_PATTERN, INVALID_USERNAME_FORMAT, YOU_DONT_HAVE_PERMISSION_TO_PERFORM_THIS_ACTION
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=False)
    class Meta:
        model = CustomUser
        fields = "__all__"

    def validate_source(self, source):
        if not source:
            raise serializers.ValidationError(SOURCE_ERROR)
        return source

    def validate_first_name(self, first_name):
        return RegexValidation(field_data=first_name, regex_pattern=FIRST_NAME_PATTERN, error_message=INVALID_FIRST_NAME).regex_validator()

    def validate_last_name(self, last_name):
        return RegexValidation(field_data=last_name, regex_pattern=LAST_NAME_PATTERN, error_message=INVALID_LAST_NAME).regex_validator()
    
    def validate_mobile_number(self, mobile_number):
        return RegexValidation(field_data=mobile_number, regex_pattern=MOBILE_NUMBER_PATTERN, error_message=INVALID_MOBILE_NUMBER).regex_validator()

    def validate_email(self, email):
        return RegexValidation(field_data=email, regex_pattern=EMAIL_PATTERN, error_message=INVALID_EMAIL_FORMAT).regex_validator()

    def validate_username(self, username):
        return RegexValidation(field_data=username, regex_pattern=EMAIL_PATTERN, error_message=INVALID_EMAIL_FORMAT).regex_validator()

    def validate_password(self, password):
        return RegexValidation(field_data=password, regex_pattern=PASSWORD_PATTERN, error_message=INVALID_PASSWORD_FORMAT).regex_validator()

    def validate_country_code(self, country_code):
        if not country_code:
            raise serializers.ValidationError(COUNTRY_CODE_MISSING)
        if country_code == "+0":
            raise serializers.ValidationError(INVALID_COUNTRY_CODE)
        return country_code
    
    def validate(self, attrs):
        if (attrs.get("country_code") and attrs.get("mobile_number") and CustomUser.objects.filter(mobile_number=attrs.get("mobile_number"), is_active=True).exists()):
            raise serializers.ValidationError(MOBILE_NUMBER_ALREADY_EXIST)
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH)
        if attrs.get('is_admin') and not self.context.get('request').user.is_superuser:
            raise serializers.ValidationError(YOU_DONT_HAVE_PERMISSION_TO_PERFORM_THIS_ACTION)
        if attrs.get('is_staff') and not self.context.get('request').user.is_superuser:
            raise serializers.ValidationError(YOU_DONT_HAVE_PERMISSION_TO_PERFORM_THIS_ACTION)
        if attrs.get('is_superuser') and not self.context.get('request').user.is_superuser:
            raise serializers.ValidationError(YOU_DONT_HAVE_PERMISSION_TO_PERFORM_THIS_ACTION)
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        return CustomUser.create_custom_user(kwargs=validated_data)

    def update(self, user_id, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(
                validated_data['password'])
        return CustomUser.update_user(user_id=user_id.id, kwargs=validated_data)

    def to_representation(self, instance):
        user_representation = super(
            UserSerializer, self).to_representation(instance=instance)
        user_representation.pop('password')
        user_representation.pop('groups')
        user_representation.pop('user_permissions')
        return user_representation


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

    def create(self, validated_data):
        return Subscription.create_subscription(kwargs=validated_data)

    def update(self, subscription_id, validated_data):
        return Subscription.update_subscription(subscription_id=subscription_id.id, kwargs=validated_data)
    

class EmailSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate_email(self, email):
        return RegexValidation(field_data=email, regex_pattern=EMAIL_PATTERN, error_message=INVALID_EMAIL_FORMAT).regex_validator()

 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = CustomUser.objects.filter(Q(username__iexact=attrs.get("username")) | Q(email__iexact=attrs.get("username"))).first()
        if user:
            if not user.is_email_verified:
                request=self.context.get('request')
                SendVerificationEmail.send_verification_email(request_site=request, user=user) 
                raise serializers.ValidationError(EMAIL_VERIFICATION_LINK_SHARED.format(email=user.email))
            else:
                data = super().validate(attrs)
                data['is_superadmin'] = user.is_superuser
                data['is_admin'] = user.is_admin
                data['is_company_details_filled'] = self.check_company_details(user_id=user.id)
                data['is_mobile_verified'] = user.is_mobile_verified
                return data
        else:
            raise serializers.ValidationError(INVALID_CREDENTIALS)
        
    def check_company_details(self, user_id):
        return True if CompanyDetails.get_company_detail(kwargs={"user_id":user_id}) else False


class ForgotPasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ["password", "confirm_password"]
       
    def validate_password(self, password):
        return RegexValidation(field_data=password, regex_pattern=PASSWORD_PATTERN, error_message=INVALID_PASSWORD_FORMAT).regex_validator()
    
    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH)
        return attrs
    
    def update(self, instance, validated_data):
        validated_data.pop('confirm_password')
        if 'password' in validated_data:
            validated_data['password'] = make_password(
                validated_data['password'])
        return CustomUser.update_user(user_id=instance.id, kwargs=validated_data)
    

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_password(self, password):
        return RegexValidation(field_data=password, regex_pattern=PASSWORD_PATTERN, error_message=INVALID_PASSWORD_FORMAT).regex_validator()
    
    def validate(self, attrs):
        request = self.context.get('request')
        user = CustomUser.get_user(kwargs={'id':request.data.get('id')})
        if check_password(attrs.get('password'), user.password):
            raise serializers.ValidationError(PASSWORD_AND_OLD_PASSWORD_ARE_SAME)
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH)
        return attrs
    
    def update(self, instance, validated_data):
        validated_data.pop('confirm_password')
        if 'password' in validated_data:
            validated_data['password'] = make_password(
                validated_data['password'])
        return CustomUser.update_user(user_id=instance.id, kwargs=validated_data)
    

class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField()

    def validate(self, attr):
        user = CustomUser.get_user(kwargs={"id":self.context.get('request').user.id})
        current_time = datetime.now(timezone.utc).replace(tzinfo=pytz.utc)
        if not user.is_mobile_verified and current_time > user.otp_expiry_time:
            raise serializers.ValidationError(OTP_IS_EXPIRED)
        if attr.get('otp') != '123456':
            raise serializers.ValidationError(INVALID_OTP)
        return attr
    
    def update(self, instance, validated_data):
        return CustomUser.update_user(user_id=instance.id, kwargs={"otp":"", 'otp_expiry_time':None, "is_mobile_verified":True})
        

# class CompanyIndustrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CompanyIndustry
#         fields = "__all__" #["industry_type"]

#     def validate_industry_type(self, industry_type):
#         return RegexValidation(field_data=industry_type, regex_pattern=FIRST_NAME_PATTERN, error_message=INVALID_INDUSTRY_NAME).regex_validator()
    
#     def create(self, validated_data):
#         return CompanyIndustry.create_company_industry(kwargs=validated_data)

#     def update(self, company_industry_id, validated_data):
#         return CompanyIndustry.update_company_industry(id=company_industry_id.id, kwargs=validated_data)


class DropDownCategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropDownCategoryItem
        fields = ["id", "item_name"]


class CompanyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = "__all__"

    def validate_company_name(self, company_name):
        return RegexValidation(field_data=company_name, regex_pattern=COMPANY_NAME_PATTERN, error_message=INVALID_COMPANY_NAME).regex_validator()

    def validate_company_industry(self, company_industry):
        if not company_industry:
            raise serializers.ValidationError(COMPANY_INDUSTRY_MISSING)
        return company_industry
    
    def validate_company_size(self, company_size):
        if not company_size:
            raise serializers.ValidationError(COMPANY_SIZE_MISSING)
        return company_size
    
    def validate_purpose(self, purpose):
        if not purpose:
            raise serializers.ValidationError(COMPANY_PURPOSE_MISSING)
        return purpose
    
    def create(self, validated_data):
        return CompanyDetails.create_company_detail(kwargs=validated_data)

    def update(self, company_detail_id, validated_data):
        return CompanyDetails.update_company_detail(id=company_detail_id.id, kwargs=validated_data)
    
    def to_representation(self, instance):
        return super().to_representation(instance)