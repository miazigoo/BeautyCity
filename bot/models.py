
from django.db import models
from django.utils import timezone


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


class Client(models.Model):
    telegram_id = models.IntegerField(unique=True)
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

    def __str__(self):
        return f"{self.name} {self.phone_number}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Appointments(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Клиент",
        related_name="client_appoinments",
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


class AboutUs(models.Model):
    salon = models.ForeignKey(
        Salons,
        on_delete=models.CASCADE,
        verbose_name="Салон",
        related_name="salon_about",
        null=True, blank=True,
    )
    descriptions = models.TextField(
        verbose_name="Описание О Нас",
        null=True, blank=True,
    )

    def __str__(self):
        return f"{self.salon.name}  {self.descriptions[:30]}"

    class Meta:
        verbose_name = "О Нас"
        verbose_name_plural = "О Нас"


class StartText(models.Model):
    descriptions = models.TextField(
        verbose_name="Стартовый текст",
        null=True, blank=True,
    )

    def __str__(self):
        return f"{self.descriptions[:30]}"

    class Meta:
        verbose_name = "Стартовый текст"
        verbose_name_plural = "Стартовые текста"


class Comment(models.Model):
    master = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
