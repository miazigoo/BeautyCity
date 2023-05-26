# Generated by Django 3.2.19 on 2023-05-26 08:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_auto_20230523_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='appointment_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 26, 11, 47, 9, 861763), verbose_name='Дата записи на услугу'),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='appointment_time',
            field=models.TimeField(choices=[(datetime.time(10, 0), '10:00'), (datetime.time(10, 30), '10:30'), (datetime.time(11, 0), '11:00'), (datetime.time(11, 30), '11:30'), (datetime.time(12, 0), '12:00'), (datetime.time(12, 30), '12:30'), (datetime.time(13, 0), '13:00'), (datetime.time(13, 30), '13:30'), (datetime.time(14, 0), '14:00'), (datetime.time(14, 30), '14:30'), (datetime.time(15, 0), '15:00'), (datetime.time(15, 30), '15:30'), (datetime.time(16, 0), '16:00'), (datetime.time(16, 30), '16:30'), (datetime.time(17, 0), '17:00'), (datetime.time(17, 30), '17:30'), (datetime.time(18, 0), '18:00'), (datetime.time(18, 30), '18:30'), (datetime.time(19, 0), '19:00'), (datetime.time(19, 30), '19:30'), (datetime.time(20, 0), '20:00'), (datetime.time(20, 30), '20:30')], verbose_name='Время записи на услугу'),
        ),
    ]
