import django_tables2 as tables
from .models import Journal


class JournalTable(tables.Table):
    class Meta:
        model = Journal
        template_name = "django_tables2/bootstrap.html"
        fields = ['student', 'date', 'theme', 'grade']
