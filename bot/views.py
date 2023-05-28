from django.shortcuts import render, get_list_or_404

from .models import Appointments


def index(request):
    appointment = get_list_or_404(Appointments)[-1]
    client_name = appointment.client.name
    client_phone = appointment.client.phone_number
    procedure_price = appointment.procedure.price

    context = {'client_name': client_name,
               'client_phone': client_phone,
               'price': procedure_price
               }

    return render(request, 'base.html', context)
