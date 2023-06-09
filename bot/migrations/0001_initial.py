from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=56, verbose_name="Имя мастера")),
            ],
            options={
                "verbose_name": "Мастер",
                "verbose_name_plural": "Мастера",
            },
        ),
        migrations.CreateModel(
            name="OpeningHours",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "work_time",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("10_00", "10_00"),
                            ("10_30", "10_30"),
                            ("11_00", "11_00"),
                            ("11_30", "11_30"),
                            ("12_00", "12_00"),
                            ("12_30", "12_30"),
                            ("13_00", "13_00"),
                            ("13_30", "13_30"),
                            ("14_00", "14_00"),
                            ("14_30", "14_30"),
                            ("15_00", "15_00"),
                            ("15_30", "15_30"),
                            ("16_00", "16_00"),
                            ("16_30", "16_30"),
                            ("17_00", "17_00"),
                            ("17_30", "17_30"),
                            ("18_00", "18_00"),
                            ("18_30", "18_30"),
                            ("19_00", "19_00"),
                            ("19_30", "19_30"),
                        ],
                        default="",
                        max_length=256,
                        null=True,
                        verbose_name="work_time",
                    ),
                ),
                ("is_busy", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Procedures",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200, verbose_name="Наименование услуги"
                    ),
                ),
                ("price", models.IntegerField(verbose_name="Стоимость услуги")),
            ],
            options={
                "verbose_name": "Услуга",
                "verbose_name_plural": "Услуги",
            },
        ),
        migrations.CreateModel(
            name="Salons",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="Название салона"),
                ),
                (
                    "address",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Адрес салона"
                    ),
                ),
            ],
            options={
                "verbose_name": "Салон",
                "verbose_name_plural": "Салоны",
            },
        ),
        migrations.CreateModel(
            name="Record",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("not_work_date", models.DateField()),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bot.employee"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="employee",
            name="procedure",
            field=models.ManyToManyField(
                related_name="masters",
                to="bot.procedures",
                verbose_name="Услуга, предоставляемая мастером",
            ),
        ),
        migrations.CreateModel(
            name="Appointments",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("telegram_id", models.IntegerField(unique=True)),
                (
                    "name",
                    models.CharField(max_length=256, null=True, verbose_name="Name"),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        verbose_name="Phone Number",
                    ),
                ),
                (
                    "appointment_date",
                    models.DateField(verbose_name="Дата записи на услугу"),
                ),
                (
                    "appointment_time",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bot.openinghours",
                        verbose_name="Время записи на услугу",
                    ),
                ),
                (
                    "master",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="master_appointments",
                        to="bot.employee",
                        verbose_name="Мастер",
                    ),
                ),
                (
                    "procedure",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="procedure_appointments",
                        to="bot.procedures",
                        verbose_name="Запись на услугу",
                    ),
                ),
                (
                    "salon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="salon_appoinments",
                        to="bot.salons",
                        verbose_name="Салон",
                    ),
                ),
            ],
            options={
                "verbose_name": "Запись к мастеру",
                "verbose_name_plural": "Записи к мастерам",
            },
        ),
    ]

