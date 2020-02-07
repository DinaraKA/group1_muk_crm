import django_filters

from accounts.models import Group
from webapp.models import Journal


class JournalFilter(django_filters.FilterSet):
    class Meta:
        model = Journal
        fields = ['discipline', 'student']

class GroupFilter(django_filters.Filter):
    class Meta:
        model = Group
        fields = ['name']