# Generated by Django 4.2.7 on 2024-01-01 19:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('question', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Envelope',
            fields=[
                ('envelope_id', models.AutoField(primary_key=True, serialize=False)),
                ('envelope_name', models.CharField(max_length=200)),
                ('envelope_query_date', models.DateField(default=datetime.date(2024, 1, 3), null=True)),
                ('envelope_frequency', models.IntegerField()),
                ('envelope_due_date', models.DateField(blank=True, null=True)),
                ('envelope_issue', models.IntegerField(default=1)),
                ('envelope_admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('questions_user', models.ManyToManyField(blank=True, to='question.userquestion')),
                ('user_answers', models.ManyToManyField(blank=True, to='question.answer')),
            ],
        ),
    ]
