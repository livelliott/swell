# Generated by Django 4.2.7 on 2024-01-01 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaultquestionenvelope',
            name='default_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]