# Generated by Django 4.2.3 on 2023-07-25 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='code',
            field=models.IntegerField(blank=True, default='', verbose_name='Последний код подтверждения'),
        ),
    ]
