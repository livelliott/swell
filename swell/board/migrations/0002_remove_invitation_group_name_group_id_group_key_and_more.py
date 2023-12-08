# Generated by Django 4.2.7 on 2023-12-08 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='group_name',
        ),
        migrations.AddField(
            model_name='group',
            name='id',
            field=models.BigAutoField(auto_created=True, default=-1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='key',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invitation',
            name='key',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
