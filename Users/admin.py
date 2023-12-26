from django.contrib import admin

from Users.models import CustomUser, Subscription, SubscriptionHistory

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(SubscriptionHistory)
admin.site.register(Subscription)