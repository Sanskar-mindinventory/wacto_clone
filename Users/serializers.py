from dataclasses import field
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from Users.models import CustomUser, Subscription
from regex_validations import RegexValidation
from Users.constants import COUNTRY_CODE_MISSING, EMAIL_PATTERN, FIRST_NAME_PATTERN, INVALID_COUNTRY_CODE, INVALID_EMAIL_FORMAT, INVALID_FIRST_NAME, INVALID_LAST_NAME, INVALID_MOBILE_NUMBER, INVALID_PASSWORD_FORMAT, LAST_NAME_PATTERN, MOBILE_NUMBER_ALREADY_EXIST, MOBILE_NUMBER_PATTERN, PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH, PASSWORD_PATTERN, SOURCE_ERROR, USERNAME_PATTERN, INVALID_USERNAME_FORMAT


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
        return RegexValidation(field_data=username, regex_pattern=USERNAME_PATTERN, error_message=INVALID_USERNAME_FORMAT).regex_validator()

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

