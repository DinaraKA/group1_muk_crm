# Generated by Django 2.2 on 2020-01-31 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200131_0937'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0018_delete_saturdaylesson'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Monday', 'Понедельник'), ('Tuesday', 'Вторник'), ('Wednesday', 'Среда'), ('Thursday', 'Четверг'), ('Friday', 'Пятница'), ('Saturday', 'Суббота')], max_length=20, verbose_name='День недели')),
                ('auditoriya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_auditoriya', to='webapp.Auditory', verbose_name='Аудитория')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_discipline', to='webapp.Discipline', verbose_name='Предмет')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_group', to='accounts.Group', verbose_name='Группа')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_lesson', to='webapp.Lesson', verbose_name='Пара')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_user', to=settings.AUTH_USER_MODEL, verbose_name='Учитель')),
            ],
        ),
    ]
