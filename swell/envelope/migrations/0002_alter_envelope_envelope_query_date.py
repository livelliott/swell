# Generated by Django 4.2.7 on 2023-12-24 02:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('envelope', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='envelope',
            name='envelope_query_date',
            field=models.DateField(default=datetime.date(2023, 12, 25), null=True),
        ),
    ]