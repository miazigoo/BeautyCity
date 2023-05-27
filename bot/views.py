from django.shortcuts import render
from .models import Appointments


def index(request):
    appointments = Appointments.objects.all()
    for appointment in appointments:
        client_name = appointment.name
        client_phone = appointment.phone_number
        procedure_price = appointment.procedure.price

        context = {'client_name': client_name,
                   'client_phone': client_phone,
                   'price': procedure_price
                   }

        return render(request, 'base.html', context)
