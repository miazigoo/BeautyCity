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
    # fields = ['appointment_date', 'appointment_time', 'master', 'procedure', 'salon', 'client']
    fieldsets = [("Дата и время процедуры", {"fields": ["appointment_date", "appointment_time"]}),
                 ("Место и испольнитель", {"fields": ["master", "salon"]}),
                 (None, {"fields": ["procedure", "client"]})]
    list_display = ("appointment_date", "appointment_time", "master", "procedure", "client")


@admin.register(Masters)
class MastersAdmin(admin.ModelAdmin):
    fields = ["name", "phone"]
    list_display = ("name", "display_procedures")
    inlines = [MastersInline]


admin.site.register(Salons)
admin.site.register(Procedures)
admin.site.register(Clients)
