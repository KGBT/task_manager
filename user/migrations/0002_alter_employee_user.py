# Generated by Django 5.0.4 on 2024-04-21 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='employee', to='user.user'),
        ),
    ]