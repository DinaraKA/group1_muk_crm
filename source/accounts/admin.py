from django.contrib import admin
from accounts.models import User, Profile, Passport, AdminPosition, UserAdminPosition, Role, SocialStatus, \
    Status, Group, Theme, Progress, ProgressOthers
from django.contrib.auth.admin import UserAdmin


# class ProfileInline(admin.StackedInline):
#     model = Profile
#     exclude = ['user']
#
#
# class ProfileAdmin(UserAdmin):
#     inlines = [ProfileInline]
#

# admin.site.unregister(User)
# admin.site.register(User, ProfileAdmin)

class ProgressAdmin(admin.ModelAdmin):
    list_display = ['pk', 'student', 'discipline']
    list_display_links = ['pk', 'student']
    search_fields = ['student__name', 'discipline__name']
    fields = ['student', 'discipline']

admin.site.register(Profile)
admin.site.register(Passport)
admin.site.register(AdminPosition)
admin.site.register(UserAdminPosition)
admin.site.register(Role)
admin.site.register(SocialStatus)
admin.site.register(Status)
admin.site.register(Group)
admin.site.register(Theme)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(ProgressOthers)