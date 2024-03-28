# Generated by Django 3.2.3 on 2024-03-28 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_genepool', '0013_alter_authorisedticketrequests_request_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authorisedticketrequests',
            name='staff_members_who_replied',
        ),
        migrations.AddField(
            model_name='authorisedticketrequests',
            name='closed_by',
            field=models.ForeignKey(default='admin', on_delete=django.db.models.deletion.CASCADE, related_name='Closed_requests', to='auth.user', verbose_name='Closed'),
            preserve_default=False,
        ),
    ]
