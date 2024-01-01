from datetime import datetime
from email.policy import default
from secrets import choice
from django.contrib import auth
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


subscription_type_choices = (
    ("Free","Free"),
    ("Standard","Standard"),
    ("Professional","Professional"),
)

subscription_plan_validity = (
    ("Free","Free"),
    ("Yearly","Yearly"),
    ("Monthly","Monthly"),
)



class Subscription(models.Model):
    subscription_plan = models.CharField(choices=subscription_type_choices, null=False, blank=False)
    payment_type = models.CharField(choices=subscription_plan_validity, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)

    @classmethod
    def get_subscription(cls, kwargs=None):
        """
        get subscription if kwargs, else get all users
        """
        return cls.objects.filter(**kwargs).first() if kwargs else cls.objects.filter()
    
    @classmethod
    def create_subscription(cls, kwargs):
        """
        create subscription with given kwargs
        """
        return cls.objects.create(**kwargs)
    
    @classmethod
    def update_subscription(cls, subscription_id, kwargs):
        """
        Update subscription with details in kwargs and return subscription
        @param subscription_id: subscription id
        """
        cls.objects.filter(id=subscription_id).update(**kwargs)
        return cls.get_subscription(kwargs={'id': subscription_id})

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False, null=False, blank=False)
    mobile_number = models.CharField(max_length=24, blank=True, null=True)
    is_mobile_verified = models.BooleanField(default=False, null=False, blank=False)
    country_code = models.CharField(max_length=24, blank=True, default="")
    source = models.CharField(max_length=32, blank=True, default="")
    is_trial_expired = models.BooleanField(
        default=False, null=True, blank=True
    )
    subscription_date = models.DateTimeField(null=True, blank=True)
    subscription_type = models.ForeignKey(Subscription ,on_delete=models.CASCADE, default=1)
    terms_and_condition = models.BooleanField(default=True, blank=False, null=False)
    is_admin = models.BooleanField(default=False, blank=False, null=False)
    otp = models.CharField(null=True, blank=True)
    otp_expiry_time = models.DateTimeField(null=True, blank=True)

    @classmethod
    def create_custom_user(cls, kwargs):
        """
        create user with given kwargs
        """
        return cls.objects.create(**kwargs)
    
    @classmethod
    def get_user(cls, kwargs=None):
        """
        get user if kwargs, else get all users
        """
        return cls.objects.filter(**kwargs).first() if kwargs else cls.objects.filter()

    @classmethod
    def update_user(cls, user_id, kwargs):
        """
        Update user with details in kwargs and return user
        @param user_id: user id
        """
        cls.objects.filter(id=user_id).update(**kwargs)
        return cls.get_user(kwargs={'id': user_id})

    @classmethod
    def set_new_password(cls, user, password):
        """
        set user password
        @param user: user
        @param password: user password
        """
        user.set_password(password)
        user.save()

class SubscriptionHistory(models.Model):
    subscription_type = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    starting_date = models.DateTimeField(null=False, blank=False)
    ending_date = models.DateTimeField(null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False)


# class CompanyIndustry(models.Model):
    # industry_type = models.CharField(max_length=100, blank=True, default="")
    # created_on = models.DateTimeField(auto_now_add=True)
    # updated_on = models.DateTimeField(auto_now=True)

    # @classmethod
    # def create_company_industry(cls, kwargs):
    #     """
    #     create user with given kwargs
    #     """
    #     return cls.objects.create(**kwargs)
    
    # @classmethod
    # def get_company_industry(cls, kwargs=None):
    #     """
    #     get user if kwargs, else get all users
    #     """
    #     return cls.objects.filter(**kwargs).first() if kwargs else cls.objects.filter()

    # @classmethod
    # def update_company_industry(cls, id, kwargs):
    #     """
    #     Update user with details in kwargs and return user
    #     @param user_id: user id
    #     """
    #     cls.objects.filter(id=id).update(**kwargs)
    #     return cls.get_company_industry(kwargs={'id': id})
    

class DropDownCategory(models.Model):
    category_name = models.CharField(max_length=100, blank=True, default="")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class DropDownCategoryItem(models.Model):
    item_name=models.CharField(max_length=100, blank=True, default="")
    category=models.ForeignKey(DropDownCategory, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @classmethod
    def get_category_items(cls, kwargs=None):
        """
        get user if kwargs, else get all users
        """
        return cls.objects.filter(**kwargs)


class CompanyDetails(models.Model):
    user = models.OneToOneField( CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=128, blank=True, default=None, null=True)
    company_website = models.CharField(max_length=128, blank=True, default=None, null=True)
    company_industry = models.ForeignKey(DropDownCategoryItem, on_delete=models.CASCADE, related_name='company_industry')
    company_size = models.ForeignKey(DropDownCategoryItem, on_delete=models.CASCADE, related_name='company_size')
    purpose = models.ForeignKey(DropDownCategoryItem, on_delete=models.CASCADE, related_name='purpose')

    @classmethod
    def create_company_detail(cls, kwargs):
        """
        create user with given kwargs
        """
        return cls.objects.create(**kwargs)
    
    @classmethod
    def get_company_detail(cls, kwargs=None):
        """
        get user if kwargs, else get all users
        """
        return cls.objects.filter(**kwargs).first() if kwargs else cls.objects.filter()

    @classmethod
    def update_company_detail(cls, id, kwargs):
        """
        Update user with details in kwargs and return user
        @param user_id: user id
        """
        cls.objects.filter(id=id).update(**kwargs)
        return cls.get_company_detail(kwargs={'id':id})