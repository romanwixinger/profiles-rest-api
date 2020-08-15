# Generated by Django 2.2 on 2020-08-15 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0011_auto_20200801_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proficiency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=1)),
                ('number_of_answers', models.IntegerField(default=0)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('subtopic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.Subtopic')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
