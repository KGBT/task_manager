# Generated by Django 4.2.13 on 2024-05-14 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_fileanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileanswer',
            name='file_answer',
            field=models.FileField(blank=True, null=True, upload_to='files_answer/'),
        ),
    ]
