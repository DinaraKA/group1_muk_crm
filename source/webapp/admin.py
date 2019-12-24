from django.contrib import admin
from accounts.models import Parent
from webapp.models import News

admin.site.register(Parent)
admin.site.register(News)

