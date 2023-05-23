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
        verbose_name_pliral = "Салоны"


class Procedures(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Наименование услуги",
        )
    price = models.IntegerField(
        verbose_name="Стоимость услуги"
        )


class Masters(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Имя мастера",
        )
    phone = models.PhoneNumberField(
        blank=True,
        null=True,
        verbose_name="Контактный номер мастера"
        )
    salon = models.ForeignKey(
        Salons,
        on_delete=models.DO_NOTHING,
        verbose_name="Салон работы мастера",
        related_name="masters"
        )
    procedure = models.ManyToManyField(
        Procedures,
        verbose_name="Услуга, предоставляемая мастером",
        related_name="procedures"
        )


class Clients(UUIDMixin, TimeStampedMixin):
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
    client = models.ForeignKey(
        Clients,
        verbose_name="Клиент",
        related_name="client_appointments",
        on_delete=models.DO_NOTHING
        )
    salon = models.ForeignKey(
        Salons,
        verbose_name="Салон",
        related_name="salon_appoinments",
        )
    appointment_datetime = models.DateTimeField(
        verbose_name="Дата и время записи на услугу",
        )
    procedure = models.ForeignKey(
        Procedures,
        verbose_name="Запись на услугу",
        related_name="procedure_appointments",
        on_delete=models.DO_NOTHING
        )