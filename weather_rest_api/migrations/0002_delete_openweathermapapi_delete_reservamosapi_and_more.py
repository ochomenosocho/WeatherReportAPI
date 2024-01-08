# Generated by Django 5.0.1 on 2024-01-06 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather_rest_api', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OpenWeatherMapAPI',
        ),
        migrations.DeleteModel(
            name='ReservamosAPI',
        ),
        migrations.RemoveField(
            model_name='city',
            name='temperatures',
        ),
        migrations.DeleteModel(
            name='WeatherReport',
        ),
    ]
