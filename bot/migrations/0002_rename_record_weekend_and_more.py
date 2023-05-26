# Generated by Django 4.2.1 on 2023-05-25 23:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Record",
            new_name="Weekend",
        ),
        migrations.AlterField(
            model_name="appointments",
            name="appointment_time",
            field=models.TimeField(verbose_name="Время записи на услугу"),
        ),
        migrations.DeleteModel(
            name="OpeningHours",
        ),
    ]