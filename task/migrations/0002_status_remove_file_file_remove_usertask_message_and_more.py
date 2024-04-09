# Generated by Django 5.0.4 on 2024-04-09 14:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=15)),
                ('message', models.TextField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='file',
            name='file',
        ),
        migrations.RemoveField(
            model_name='usertask',
            name='message',
        ),
        migrations.AddField(
            model_name='file',
            name='path',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='usertask',
            name='status',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='task.status'),
        ),
    ]