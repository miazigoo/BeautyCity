from django.contrib import admin

from .models import (
    Salons,
    Employee,
    Procedures,
    Appointments,
    Weekend,
    AboutUs, StartText, Client
)


class MastersInline(admin.TabularInline):
    model = Procedures.masters.through


@admin.register(Employee)
class MastersAdmin(admin.ModelAdmin):
    fields = ["name", ]
    list_display = ("name", "display_procedures")
    inlines = [MastersInline]


@admin.register(Appointments)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ("appointment_date", "appointment_time", "master", "procedure")


admin.site.register(Salons)
admin.site.register(Procedures)
admin.site.register(Weekend)
admin.site.register(AboutUs)
admin.site.register(StartText)
admin.site.register(Client)
