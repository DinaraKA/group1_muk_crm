import django_tables2 as tables
from .models import Journal
# from django_tables2.utils import A # alias for Accessor


# class PersonalGradesTable(tables.Table):
#     class Meta:
#         model = Journal
#         template_name = "django_tables2/bootstrap.html"
#         fields = ("discipline", "date", "grade")

class PersonColumn(tables.Column):
    attrs = {
        # 'th': {'date': lambda record: record.date},
        'td': {
        'data-discipline': lambda record: record.discipline,
        'data-grade': lambda record: record.grade
    }
    }
    def render(self, record):
        return '{} {}'.format(record.discipline, record.grade)

class PersonalGradesTable(tables.Table):
    aisl = PersonColumn()

    class Meta:
        model = Journal
        # name = tables.Column(attrs={"th": {"id": "date"}})

        template_name = "django_tables2/bootstrap.html"
        # fields = ("discipline", "date", "grade")

