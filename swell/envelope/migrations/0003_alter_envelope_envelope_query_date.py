# Generated by Django 4.2.7 on 2024-01-03 03:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('envelope', '0002_envelope_questions_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='envelope',
            name='envelope_query_date',
            field=models.DateField(default=datetime.date(2024, 1, 4), null=True),
        ),
    ]
