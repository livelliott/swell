# Generated by Django 4.2.7 on 2023-12-24 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_basequestion_envelope_issue_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basequestion',
            name='envelope_issue_number',
        ),
    ]
