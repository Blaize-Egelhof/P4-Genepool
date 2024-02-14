# Generated by Django 3.2.3 on 2024-02-14 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_genepool', '0005_alter_authorisedquoterequests_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorisedquoterequests',
            name='status',
            field=models.CharField(blank=True, choices=[('Unanswered', 'Open'), ('Answered', 'Ongoing'), ('Closed', 'Closed')], default='Ongoing', max_length=20),
        ),
    ]
