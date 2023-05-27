from django.db import models


class Salons(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название салона"
    )
    address = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Адрес салона"
    )

    def __str__(self):
        return f"{self.name}, {self.address}"

    class Meta:
        verbose_name = "Салон"
        verbose_name_plural = "Салоны"


class Procedures(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Наименование услуги",
    )
    price = models.IntegerField(
        verbose_name="Стоимость услуги"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Employee(models.Model):
    name = models.CharField(
        max_length=56,
        verbose_name="Имя мастера",
    )
    procedure = models.ManyToManyField(
        Procedures,
        verbose_name="Услуга, предоставляемая мастером",
        related_name="masters",
    )

    def __str__(self):
        return self.name

    def display_procedures(self):
        return ', '.join([str(procedure.name) for procedure in self.procedure.all()])

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"


class WeekendQuerySet(models.QuerySet):

    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except Weekend.DoesNotExist:
            return None


class Weekend(models.Model):
    employee = models.ForeignKey(Employee, models.CASCADE)
    not_work_date = models.DateField()
    objects = WeekendQuerySet.as_manager()

    def __str__(self):
        return f'Выходной: {self.employee} {self.not_work_date}'

    class Meta:
        verbose_name = 'Выходной'
        verbose_name_plural = 'Выходные'


class Appointments(models.Model):
    telegram_id = models.IntegerField()
    name = models.CharField(
        max_length=256,
        null=True,
        blank=False,
        verbose_name="Name"
    )
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Phone Number"
    )
    salon = models.ForeignKey(
        Salons,
        on_delete=models.CASCADE,
        verbose_name="Салон",
        related_name="salon_appoinments",
    )
    appointment_date = models.DateField(
        verbose_name="Дата записи на услугу",
        )
    appointment_time = models.TimeField(
        verbose_name="Время записи на услугу",
        )
    procedure = models.ForeignKey(
        Procedures,
        null=True,
        blank=True,
        verbose_name="Запись на услугу",
        related_name="procedure_appointments",
        on_delete=models.CASCADE
    )
    master = models.ForeignKey(
        Employee,
        verbose_name="Мастер",
        related_name="master_appointments",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.appointment_date} {self.appointment_time}, {self.master}"

    class Meta:
        verbose_name = "Запись к мастеру"
        verbose_name_plural = "Записи к мастерам"
