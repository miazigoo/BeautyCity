# Generated by Django 3.2.19 on 2023-05-23 18:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointments',
            options={'verbose_name': 'Запись к мастеру', 'verbose_name_plural': 'Записи к мастерам'},
        ),
        migrations.AlterModelOptions(
            name='masters',
            options={'verbose_name': 'Мастер', 'verbose_name_plural': 'Мастера'},
        ),
        migrations.AlterModelOptions(
            name='procedures',
            options={'verbose_name': 'Услуга', 'verbose_name_plural': 'Услуги'},
        ),
        migrations.RemoveField(
            model_name='appointments',
            name='appointment_datetime',
        ),
        migrations.AddField(
            model_name='appointments',
            name='appointment_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 23, 21, 39, 13, 984169), verbose_name='Дата записи на услугу'),
        ),
        migrations.AddField(
            model_name='appointments',
            name='appointment_time',
            field=models.TimeField(default=datetime.datetime(2023, 5, 23, 21, 39, 13, 984168), verbose_name='Время записи на услугу'),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='client_appointments', to='bot.clients', verbose_name='Клиент'),
        ),
    ]
