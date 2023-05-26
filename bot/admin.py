from django.contrib import admin

from .models import (
    Clients,
    Salons,
    Masters,
    Procedures,
    Appointments
)


class MastersInline(admin.TabularInline):
    model = Procedures.masters.through


@admin.register(Appointments)
class AppointmentAdmin(admin.ModelAdmin):
    fieldsets = [("Дата и время процедуры", {"fields": ["appointment_date", "appointment_time"]}),
                 ("Место и испольнитель", {"fields": ["master", "salon"]}),
                 (None, {"fields": ["procedure", "client"]})]
    list_display = ("appointment_date", "appointment_time", "master", "procedure", "client")


@admin.register(Masters)
class MastersAdmin(admin.ModelAdmin):
    fieldsets = [("Контактные данные", {"fields": ["name", "phone"]}),
            # ("Услуги", {"fields": ("MastersInline")}),
            ("Расписание по неделе", {"fields": ["mon", "tue", "wed", "thu", "fry", "sat", "sun"]}),
            ]

    list_display = ("name", "display_procedures")
    inlines = [MastersInline]


admin.site.register(Salons)
admin.site.register(Procedures)
admin.site.register(Clients)
