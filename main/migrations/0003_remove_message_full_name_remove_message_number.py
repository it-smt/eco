# Generated by Django 4.2.3 on 2023-07-24 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='message',
            name='number',
        ),
    ]
