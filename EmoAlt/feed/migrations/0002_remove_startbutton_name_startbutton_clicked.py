# Generated by Django 4.2.7 on 2023-11-19 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='startbutton',
            name='name',
        ),
        migrations.AddField(
            model_name='startbutton',
            name='clicked',
            field=models.BooleanField(default=False),
        ),
    ]
