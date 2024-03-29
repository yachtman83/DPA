from django.contrib import admin

from main.models import UserProfile, Course, Subscription

admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Subscription)