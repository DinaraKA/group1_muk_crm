from django.contrib import admin
from accounts.models import Profile, Passport, AdminPosition, UserAdminPosition, Role, UserRole, SocialStatus, \
    UserSocialStatus


admin.site.register(Profile)
admin.site.register(Passport)
admin.site.register(AdminPosition)
admin.site.register(UserAdminPosition)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(SocialStatus)
admin.site.register(UserSocialStatus)