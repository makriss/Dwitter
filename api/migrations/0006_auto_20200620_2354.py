# Generated by Django 3.0.7 on 2020-06-20 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='liked_by',
            field=models.TextField(default='', verbose_name='Liked By'),
        ),
        migrations.AlterUniqueTogether(
            name='likes',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='likes',
            name='last_update',
        ),
        migrations.RemoveField(
            model_name='likes',
            name='user_id',
        ),
    ]
