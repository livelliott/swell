# Generated by Django 4.2.9 on 2024-01-13 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('envelope', '0008_rename_envelope_query_date_future_envelope_change_envelope_query_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datemanager',
            old_name='change_query_date',
            new_name='change_dates',
        ),
    ]