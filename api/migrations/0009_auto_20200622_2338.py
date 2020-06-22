# Generated by Django 3.0.7 on 2020-06-22 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0008_auto_20200621_1301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='liked_by',
        ),
        migrations.AddField(
            model_name='likes',
            name='user_id',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
