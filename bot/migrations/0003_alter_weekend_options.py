# Generated by Django 4.2.1 on 2023-05-25 23:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0002_rename_record_weekend_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="weekend",
            options={"verbose_name": "Выходной", "verbose_name_plural": "Выходные"},
        ),
    ]
