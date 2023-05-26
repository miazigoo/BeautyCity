# Generated by Django 3.2.19 on 2023-05-26 11:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_auto_20230526_1403'),
    ]

    operations = [
        migrations.RenameField(
            model_name='masters',
            old_name='sut',
            new_name='sat',
        ),
        migrations.AlterField(
            model_name='appointments',
            name='appointment_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 26, 14, 13, 33, 76357), verbose_name='Дата записи на услугу'),
        ),
    ]
