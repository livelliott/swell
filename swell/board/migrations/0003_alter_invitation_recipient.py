# Generated by Django 4.2.7 on 2023-12-10 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0002_alter_group_envelope_id_alter_invitation_recipient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='recipient',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_invitations', to=settings.AUTH_USER_MODEL),
        ),
    ]
