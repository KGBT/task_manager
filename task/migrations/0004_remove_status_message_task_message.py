# Generated by Django 5.0.4 on 2024-05-05 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_task_initiator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='message',
        ),
        migrations.AddField(
            model_name='task',
            name='message',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]