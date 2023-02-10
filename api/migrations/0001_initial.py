# Generated by Django 4.1.6 on 2023-02-09 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDateTime', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('date', models.DateField(blank=True)),
                ('max', models.IntegerField(blank=True, default=0)),
                ('min', models.IntegerField(blank=True, default=0)),
                ('percipitation', models.IntegerField(blank=True, default=0)),
                ('station', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(unique=True)),
                ('avg_max', models.IntegerField()),
                ('avg_min', models.IntegerField()),
                ('total_percipitation', models.IntegerField()),
            ],
        ),
        migrations.AddConstraint(
            model_name='weatherdetail',
            constraint=models.UniqueConstraint(fields=('date', 'station'), name='station_date_unique'),
        ),
    ]