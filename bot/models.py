import datetime

from django.db import models

from phonenumber_field.modelfields import PhoneNumberField



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


class Masters(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Имя мастера",
        )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name="Контактный номер мастера"
        )
    procedure = models.ManyToManyField(
        Procedures,
        verbose_name="Услуга, предоставляемая мастером",
        related_name="masters",
        # on_delete=models.DO_NOTHING
        )
    mon = models.BooleanField(
        verbose_name="Понедельник",
        default=True,
        blank=True,
        )
    tue = models.BooleanField(
        verbose_name="Вторник",
        default=True,
        blank=True,
        )
    wed = models.BooleanField(
        verbose_name="Среда",
        default=True,
        blank=True,
        )
    thu = models.BooleanField(
        verbose_name="Черверг",
        default=True,
        blank=True,
        )
    fry = models.BooleanField(
        verbose_name="Пятница",
        default=True,
        blank=True,
        )
    sat = models.BooleanField(
        verbose_name="Суббота",
        default=True,
        blank=True,
        )
    sun = models.BooleanField(
        verbose_name="Воскресенье",
        default=True,
        blank=True,
        )

    def __str__(self):
        return self.name

    def display_procedures(self):
        return ', '.join([str(procedure.name) for procedure in self.procedure.all()])

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"


class Clients(models.Model):
    telegram_id = models.IntegerField(unique=True)
    username = models.CharField(
        max_length=64,
        null=True,
        blank=False,
        verbose_name="User Name"
        )
    first_name = models.CharField(
        max_length=256,
        null=True,
        blank=False,
        verbose_name="First Name"
        )
    last_name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name="Last Name"
        )
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Phone Number"
        )
    email = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="email"
        )
    is_admin = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        verbose_name="Администратор"
        )

    def __str__(self):
        if self.username:
            return f'@{self.username}'
        else:
            return f'{self.telegram_id}'

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Appointments(models.Model):
    set_time = (
        (datetime.time(10,0,0), "10:00"), (datetime.time(10,30,0), "10:30"),
        (datetime.time(11,0,0), "11:00"), (datetime.time(11,30,0), "11:30"),
        (datetime.time(12,0,0), "12:00"), (datetime.time(12,30,0), "12:30"),
        (datetime.time(13,0,0), "13:00"), (datetime.time(13,30,0), "13:30"),
        (datetime.time(14,0,0), "14:00"), (datetime.time(14,30,0), "14:30"),
        (datetime.time(15,0,0), "15:00"), (datetime.time(15,30,0), "15:30"),
        (datetime.time(16,0,0), "16:00"), (datetime.time(16,30,0), "16:30"),
        (datetime.time(17,0,0), "17:00"), (datetime.time(17,30,0), "17:30"),
        (datetime.time(18,0,0), "18:00"), (datetime.time(18,30,0), "18:30"),
        (datetime.time(19,0,0), "19:00"), (datetime.time(19,30,0), "19:30"),
        (datetime.time(20,0,0), "20:00"), (datetime.time(20,30,0), "20:30"),
        )
    client = models.ForeignKey(
        Clients,
        null=True,
        blank=True,
        verbose_name="Клиент",
        related_name="client_appointments",
        on_delete=models.DO_NOTHING
        )
    salon = models.ForeignKey(
        Salons,
        verbose_name="Салон",
        related_name="salon_appoinments",
        on_delete=models.DO_NOTHING
        )
    appointment_date = models.DateField(
        verbose_name="Дата записи на услугу",
        default=datetime.datetime.today()
        )
    appointment_time = models.TimeField(
        verbose_name="Время записи на услугу",
        choices=set_time,
        )
    procedure = models.ForeignKey(
        Procedures,
        null=True,
        blank=True,
        verbose_name="Запись на услугу",
        related_name="procedure_appointments",
        on_delete=models.DO_NOTHING
        )
    master = models.ForeignKey(
        Masters,
        verbose_name="Мастер",
        related_name="master_appointments",
        on_delete=models.DO_NOTHING
    )

    # def choices(self):
    #     if self.appointment_date == datetime.datetime.today():


    def __str__(self):
        return f"{self.appointment_date} {self.appointment_time}, {self.master}"

    class Meta:
        verbose_name = "Запись к мастеру"
        verbose_name_plural = "Записи к мастерам"
