# Generated by Django 4.2.7 on 2023-11-18 04:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BrainWave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='WavePoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wave', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.brainwave')),
            ],
        ),
        migrations.CreateModel(
            name='WaveValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.wavepoint')),
            ],
        ),
        migrations.CreateModel(
            name='WaveTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.FloatField()),
                ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.wavepoint')),
            ],
        ),
    ]
