# Generated by Django 3.2.3 on 2024-02-20 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_genepool', '0009_auto_20240219_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatDialogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(blank=True, upload_to='../GENEPOOL/templates/ticket-files/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='authorisedticketrequests',
            name='status',
            field=models.CharField(choices=[('Unanswered', 'Unanswered'), ('Answered', 'Answered'), ('Closed', 'Closed')], default='Unanswered', max_length=20),
        ),
        migrations.DeleteModel(
            name='TicketFile',
        ),
        migrations.AddField(
            model_name='chatdialogue',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_dialogues', to='app_genepool.authorisedticketrequests'),
        ),
    ]
