# Generated by Django 4.2.7 on 2023-12-25 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='is_accepted',
        ),
    ]