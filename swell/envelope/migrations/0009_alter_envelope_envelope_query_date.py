# Generated by Django 4.2.7 on 2023-12-26 20:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('envelope', '0008_alter_envelope_envelope_query_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='envelope',
            name='envelope_query_date',
            field=models.DateField(default=datetime.date(2023, 12, 28), null=True),
        ),
    ]
