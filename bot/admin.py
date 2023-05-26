from django.contrib import admin

from .models import (
    Salons,
    Employee,
    Procedures,
    Appointments,
    Weekend
)


class MastersInline(admin.TabularInline):
    model = Procedures.masters.through


@admin.register(Employee)
class MastersAdmin(admin.ModelAdmin):
    fields = ["name", ]
    list_display = ("name", "display_procedures")
    inlines = [MastersInline]


admin.site.register(Salons)
admin.site.register(Procedures)
admin.site.register(Weekend)
admin.site.register(Appointments)
