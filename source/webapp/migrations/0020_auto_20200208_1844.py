# Generated by Django 2.2 on 2020-02-08 18:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20200208_1844'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0019_schedule'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together={('lesson', 'day', 'group'), ('lesson', 'day', 'auditoriya'), ('lesson', 'day', 'teacher')},
        ),
    ]
