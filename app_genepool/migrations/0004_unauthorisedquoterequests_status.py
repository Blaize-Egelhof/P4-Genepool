# Generated by Django 3.2.22 on 2023-11-13 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_genepool', '0003_unauthorisedquoterequests_request_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='unauthorisedquoterequests',
            name='status',
            field=models.CharField(blank=True, default='Open', max_length=20),
        ),
    ]
