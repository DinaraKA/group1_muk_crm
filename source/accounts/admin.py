from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Passport, ParentOne, ParentTwo


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = []
    exclude = ['passport']


class PassportInline(admin.StackedInline):
    model = Passport
    fields = []


class ParrentOneInline(admin.StackedInline):
    model = ParentOne
    fields = []


class ParrentTwoInline(admin.StackedInline):
    model = ParentTwo
    fields = []


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline, PassportInline]


admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
admin.site.register(Passport)